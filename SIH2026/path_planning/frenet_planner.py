import numpy as np

class QuinticPolynomial:
    """Quintic Polynomial for smooth jerk-minimizing trajectory generation."""
    def __init__(self, xs, vxs, axs, xe, vxe, axe, time):
        self.a0 = xs
        self.a1 = vxs
        self.a2 = axs / 2.0

        A = np.array([
            [time ** 3, time ** 4, time ** 5],
            [3 * time ** 2, 4 * time ** 3, 5 * time ** 4],
            [6 * time, 12 * time ** 2, 20 * time ** 3]
        ])
        b = np.array([
            xe - self.a0 - self.a1 * time - self.a2 * time ** 2,
            vxe - self.a1 - 2 * self.a2 * time,
            axe - 2 * self.a2
        ])

        try:
            x = np.linalg.solve(A, b)
            self.a3 = x[0]
            self.a4 = x[1]
            self.a5 = x[2]
        except np.linalg.LinAlgError:
            self.a3, self.a4, self.a5 = 0.0, 0.0, 0.0

    def calc_point(self, t):
        return self.a0 + self.a1 * t + self.a2 * t ** 2 + self.a3 * t ** 3 + self.a4 * t ** 4 + self.a5 * t ** 5

    def calc_first_derivative(self, t):
        return self.a1 + 2 * self.a2 * t + 3 * self.a3 * t ** 2 + 4 * self.a4 * t ** 3 + 5 * self.a5 * t ** 4

    def calc_second_derivative(self, t):
        return 2 * self.a2 + 6 * self.a3 * t + 12 * self.a4 * t ** 2 + 20 * self.a5 * t ** 3

    def calc_third_derivative(self, t):
        return 6 * self.a3 + 24 * self.a4 * t + 60 * self.a5 * t ** 2


class QuarticPolynomial:
    """Quartic Polynomial for speed/longitudinal profile generation."""
    def __init__(self, xs, vxs, axs, vxe, axe, time):
        self.a0 = xs
        self.a1 = vxs
        self.a2 = axs / 2.0

        A = np.array([
            [3 * time ** 2, 4 * time ** 3],
            [6 * time, 12 * time ** 2]
        ])
        b = np.array([
            vxe - self.a1 - 2 * self.a2 * time,
            axe - 2 * self.a2
        ])

        try:
            x = np.linalg.solve(A, b)
            self.a3 = x[0]
            self.a4 = x[1]
        except np.linalg.LinAlgError:
            self.a3, self.a4 = 0.0, 0.0

    def calc_point(self, t):
        return self.a0 + self.a1 * t + self.a2 * t ** 2 + self.a3 * t ** 3 + self.a4 * t ** 4

    def calc_first_derivative(self, t):
        return self.a1 + 2 * self.a2 * t + 3 * self.a3 * t ** 2 + 4 * self.a4 * t ** 3

    def calc_second_derivative(self, t):
        return 2 * self.a2 + 6 * self.a3 * t + 12 * self.a4 * t ** 2

    def calc_third_derivative(self, t):
        return 6 * self.a3 + 24 * self.a4 * t


class FrenetPath:
    def __init__(self):
        self.t = []
        self.d = []
        self.d_d = []
        self.d_dd = []
        self.d_ddd = []
        self.s = []
        self.s_d = []
        self.s_dd = []
        self.s_ddd = []
        self.cd = 0.0
        self.cv = 0.0
        self.cf = 0.0
        self.x = []
        self.y = []
        self.yaw = []
        self.ds = []
        self.c = []


class FrenetOptimalTrajectoryPlanner:
    """
    Adaptive Local Path Planner in Frenet coordinates.
    Evaluates candidate polynomial curves to find minimum-cost collision-free path.
    """
    def __init__(self, max_speed=15.0, max_accel=3.5, max_curvature=0.4, dt=0.2):
        self.max_speed = max_speed
        self.max_accel = max_accel
        self.max_curvature = max_curvature
        self.dt = dt

        # Cost weights
        self.k_jerk = 0.1
        self.k_time = 0.1
        self.k_diff = 1.0
        self.k_lat = 1.0
        self.k_lon = 1.0
        self.k_obs = 100.0

    def plan(self, s0, c_speed, c_d, c_d_d, c_d_dd, target_speed, target_d, obstacles, min_t=2.0, max_t=4.0):
        """
        Generates best collision-free trajectory.
        """
        frenet_paths = []

        # Sample lateral offsets and planning time horizons
        d_samples = [target_d, target_d - 0.5, target_d + 0.5] if target_d != 0 else [0.0, -1.0, 1.0, -2.0, 2.0]
        
        for di in d_samples:
            for Ti in np.arange(min_t, max_t + 0.5, 1.0):
                fp = FrenetPath()
                lat_poly = QuinticPolynomial(c_d, c_d_d, c_d_dd, di, 0.0, 0.0, Ti)

                fp.t = [t for t in np.arange(0.0, Ti, self.dt)]
                fp.d = [lat_poly.calc_point(t) for t in fp.t]
                fp.d_d = [lat_poly.calc_first_derivative(t) for t in fp.t]
                fp.d_dd = [lat_poly.calc_second_derivative(t) for t in fp.t]
                fp.d_ddd = [lat_poly.calc_third_derivative(t) for t in fp.t]

                lon_poly = QuarticPolynomial(s0, c_speed, 0.0, target_speed, 0.0, Ti)
                fp.s = [lon_poly.calc_point(t) for t in fp.t]
                fp.s_d = [lon_poly.calc_first_derivative(t) for t in fp.t]
                fp.s_dd = [lon_poly.calc_second_derivative(t) for t in fp.t]
                fp.s_ddd = [lon_poly.calc_third_derivative(t) for t in fp.t]

                # Convert (s, d) to Global Cartesian (x, y) assuming longitudinal reference axis
                fp.x = list(fp.s)
                fp.y = list(fp.d)
                
                # Approximate yaw
                for idx in range(len(fp.x) - 1):
                    dx = fp.x[idx + 1] - fp.x[idx]
                    dy = fp.y[idx + 1] - fp.y[idx]
                    fp.yaw.append(np.arctan2(dy, max(dx, 1e-3)))
                if fp.yaw:
                    fp.yaw.append(fp.yaw[-1])
                else:
                    fp.yaw.append(0.0)

                # Cost Calculation
                jerk_lat = sum(np.array(fp.d_ddd) ** 2)
                jerk_lon = sum(np.array(fp.s_ddd) ** 2)
                speed_diff = sum((target_speed - np.array(fp.s_d)) ** 2)
                target_d_diff = sum((target_d - np.array(fp.d)) ** 2)

                fp.cd = self.k_jerk * jerk_lat + self.k_time * Ti + self.k_diff * target_d_diff
                fp.cv = self.k_jerk * jerk_lon + self.k_time * Ti + self.k_diff * speed_diff
                fp.cf = self.k_lat * fp.cd + self.k_lon * fp.cv

                # Collision check
                collision = False
                for ox, oy, r in obstacles:
                    for px, py in zip(fp.x, fp.y):
                        dist = np.hypot(px - ox, py - oy)
                        if dist <= r:
                            collision = True
                            break
                    if collision:
                        break

                if not collision:
                    frenet_paths.append(fp)

        if not frenet_paths:
            # Fallback safe trajectory (brake smoothly)
            fallback = FrenetPath()
            Ti = 2.5
            fallback.t = [t for t in np.arange(0.0, Ti, self.dt)]
            lon_poly = QuarticPolynomial(s0, c_speed, -2.0, 0.0, 0.0, Ti)
            fallback.s = [lon_poly.calc_point(t) for t in fallback.t]
            fallback.s_d = [lon_poly.calc_first_derivative(t) for t in fallback.t]
            fallback.d = [c_d for _ in fallback.t]
            fallback.x = list(fallback.s)
            fallback.y = list(fallback.d)
            fallback.yaw = [0.0 for _ in fallback.t]
            return fallback

        # Pick path with lowest total cost
        best_path = min(frenet_paths, key=lambda p: p.cf)
        return best_path
