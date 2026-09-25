import numpy as np

class TrackedActor:
    def __init__(self, track_id, class_name, x, y, vx=0.0, vy=0.0):
        self.track_id = track_id
        self.class_name = class_name
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.history = [(x, y)]
        self.missed_frames = 0
        self.age = 1

    def update(self, detected_obj, dt=0.1):
        # Kalman filter alpha-beta smoothing
        alpha = 0.7
        beta = 0.5
        
        dx = detected_obj.x - self.x
        dy = detected_obj.y - self.y
        
        meas_vx = dx / max(dt, 1e-4)
        meas_vy = dy / max(dt, 1e-4)

        self.x += alpha * dx
        self.y += alpha * dy
        self.vx += beta * (meas_vx - self.vx)
        self.vy += beta * (meas_vy - self.vy)
        
        self.history.append((self.x, self.y))
        if len(self.history) > 30:
            self.history.pop(0)
            
        self.missed_frames = 0
        self.age += 1

class MultiObjectTracker:
    """Kalman Filter & Proximity-based Multi-Object Tracker (similar to ByteTrack)."""
    def __init__(self, max_missed=5, match_dist_thresh=3.0):
        self.tracks = {}
        self.next_track_id = 1
        self.max_missed = max_missed
        self.match_dist_thresh = match_dist_thresh

    def step(self, detected_objects, dt=0.1):
        unmatched_detections = list(detected_objects)
        matched_tracks = set()

        # Match existing tracks with detections
        for track_id, track in list(self.tracks.items()):
            best_det = None
            min_dist = float('inf')

            for det in unmatched_detections:
                dist = np.hypot(track.x - det.x, track.y - det.y)
                if dist < min_dist and dist < self.match_dist_thresh:
                    min_dist = dist
                    best_det = det

            if best_det:
                track.update(best_det, dt=dt)
                matched_tracks.add(track_id)
                unmatched_detections.remove(best_det)
            else:
                track.missed_frames += 1
                # Dead reckoning for missed frames
                track.x += track.vx * dt
                track.y += track.vy * dt

        # Remove stale tracks
        self.tracks = {tid: t for tid, t in self.tracks.items() if t.missed_frames <= self.max_missed}

        # Create new tracks for unmatched detections
        for det in unmatched_detections:
            new_track = TrackedActor(self.next_track_id, det.class_name, det.x, det.y, det.vx, det.vy)
            self.tracks[self.next_track_id] = new_track
            self.next_track_id += 1

        return list(self.tracks.values())
