class SnapshotArray:

    def __init__(self, length: int):
        self.arr = {}
        self.snaps = {}
        self.snap_id = 0
        self.set_id = 0

    def set(self, index: int, val: int) -> None:
        self.arr[index] = val
        self.set_id += 1

    def snap(self) -> int:
        if self.snap_id > 0:
            prev_snap = self.snaps[self.snap_id - 1]
            if prev_snap[0] == self.set_id:
                self.snaps[self.snap_id] = self.snaps[self.snap_id - 1]
                self.snap_id += 1
                return self.snap_id - 1

        self.snaps[self.snap_id] = (
            self.set_id, 
            {idx: val for idx, val in self.arr.items() if val != 0}
        )
        self.snap_id += 1

        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        snap = self.snaps[snap_id]
        return snap[1].get(index, 0)


# Your SnapshotArray object will be instantiated and called as such:
# obj = SnapshotArray(length)
# obj.set(index,val)
# param_2 = obj.snap()
# param_3 = obj.get(index,snap_id)