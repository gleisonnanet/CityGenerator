# To support reload properly, try to access a package var, 
# if it's there, reload everything
if "JointHouseBlock" in locals():
    import imp
    imp.reload(block)
    imp.reload(const)
    imp.reload(parcel)
else:
    from city_generator import block, const, parcel


import bpy
import random

class JointHouseBlock(block.Block):
    """Class managing the blocks of joint houses."""
    
    def __init__(self, x_start, x_size, y_start, y_size, city):
        """Create a new block of joint houses."""
        
        block.Block.__init__(self, x_start, x_size, y_start, y_size,
                             city)
        
        self.draw()
        self.draw_grass()
        self.parcel()
    
    
    def parcel(self):
        """Cut it into parcels.
        We first create the corner buildings. Then, we fill the road
        sides with buildings in such a way that they don't collide."""
        
        # create the corner buildings
        min_corner_size = const.min_joint_house_size
        max_corner_size = min(
            (self.parcels_x_size - const.min_joint_house_size)/2,
            (self.parcels_y_size - const.min_joint_house_size)/2,
            const.max_joint_house_corner_size
        )
        corner_building_sizes = list((0, 0, 0, 0))
        for i in range(4):
            corner_building_sizes[i] = random.triangular(
                (min_corner_size+max_corner_size)/2, max_corner_size)
        # S-W corner
        parcel.Parcel(self.parcels_x_start, corner_building_sizes[0],
                      self.parcels_y_start, corner_building_sizes[0],
                      0, self, "joint_house_corner")
        # S-E corner
        parcel.Parcel(self.parcels_x_start + self.parcels_x_size \
                        - corner_building_sizes[1],
                      corner_building_sizes[1],
                      self.parcels_y_start,
                      corner_building_sizes[1], 1, self,
                      "joint_house_corner")
        # N-E corner
        parcel.Parcel(self.parcels_x_start + self.parcels_x_size \
                        - corner_building_sizes[2],
                      corner_building_sizes[2],
                      self.parcels_y_start + self.parcels_y_size \
                      - corner_building_sizes[2],
                      corner_building_sizes[2], 2, self,
                      "joint_house_corner")
        # N-W corner
        parcel.Parcel(self.parcels_x_start,
                      corner_building_sizes[3],
                      self.parcels_y_start + self.parcels_y_size \
                        - corner_building_sizes[3],
                      corner_building_sizes[3], 3, self,
                      "joint_house_corner")
        
        # create the other buildings
        # S face
        parcels_side_x_sizes = self.cut_length(
            self.parcels_x_size - corner_building_sizes[0] \
                - corner_building_sizes[1],
            const.min_joint_house_size,
            const.max_joint_house_width
        )
        parcels_side_x_starts = list(parcels_side_x_sizes)
        temp_x_start = self.parcels_x_start + corner_building_sizes[0]
        for i in range(len(parcels_side_x_sizes)):
            parcels_side_x_starts[i] = temp_x_start
            temp_x_start = temp_x_start + parcels_side_x_sizes[i]
            parcel_y_size = random.triangular(
                const.min_joint_house_size,
                min(parcels_side_x_starts[i] - self.parcels_x_start,
                    self.parcels_x_start + self.parcels_x_size \
                        - (parcels_side_x_starts[i] +
                            parcels_side_x_sizes[i]),
                    self.parcels_y_size/2,
                    const.max_joint_house_depth))
            parcel.Parcel(parcels_side_x_starts[i],
                          parcels_side_x_sizes[i],
                          self.parcels_y_start,
                          parcel_y_size, 0, self,
                          "joint_house_side")
        # E face
        parcels_side_y_sizes = self.cut_length(
            self.parcels_y_size - corner_building_sizes[1] \
                - corner_building_sizes[2],
            const.min_joint_house_size,
            const.max_joint_house_width
        )
        parcels_side_y_starts = list(parcels_side_y_sizes)
        temp_y_start = self.parcels_y_start + corner_building_sizes[1]
        for i in range(len(parcels_side_y_sizes)):
            parcels_side_y_starts[i] = temp_y_start
            temp_y_start = temp_y_start + parcels_side_y_sizes[i]
            parcel_x_size = random.triangular(
                const.min_joint_house_size,
                min(parcels_side_y_starts[i] - self.parcels_y_start,
                    self.parcels_y_start + self.parcels_y_size \
                        - (parcels_side_y_starts[i] +
                            parcels_side_y_sizes[i]),
                    self.parcels_x_size/2,
                    const.max_joint_house_depth,))
            parcel.Parcel(self.parcels_x_start + self.parcels_x_size \
                              - parcel_x_size,
                          parcel_x_size,
                          parcels_side_y_starts[i],
                          parcels_side_y_sizes[i], 1, self,
                          "joint_house_side")
        # N face
        parcels_side_x_sizes = self.cut_length(
            self.parcels_x_size - corner_building_sizes[2] \
                - corner_building_sizes[3],
            const.min_joint_house_size,
            const.max_joint_house_width
        )
        parcels_side_x_starts = list(parcels_side_x_sizes)
        temp_x_start = self.parcels_x_start + corner_building_sizes[3]
        for i in range(len(parcels_side_x_sizes)):
            parcels_side_x_starts[i] = temp_x_start
            temp_x_start = temp_x_start + parcels_side_x_sizes[i]
            parcel_y_size = random.triangular(
                const.min_joint_house_size,
                min(parcels_side_x_starts[i] - self.parcels_x_start,
                    self.parcels_x_start + self.parcels_x_size \
                        - (parcels_side_x_starts[i] +
                            parcels_side_x_sizes[i]),
                    self.parcels_y_size/2,
                    const.max_joint_house_depth))
            parcel.Parcel(parcels_side_x_starts[i],
                          parcels_side_x_sizes[i],
                          self.parcels_y_start + self.parcels_y_size \
                              - parcel_y_size,
                          parcel_y_size, 2, self,
                          "joint_house_side")
        # W face
        parcels_side_y_sizes = self.cut_length(
            self.parcels_y_size - corner_building_sizes[3] \
                - corner_building_sizes[0],
            const.min_joint_house_size,
            const.max_joint_house_width
        )
        parcels_side_y_starts = list(parcels_side_y_sizes)
        temp_y_start = self.parcels_y_start + corner_building_sizes[0]
        for i in range(len(parcels_side_y_sizes)):
            parcels_side_y_starts[i] = temp_y_start
            temp_y_start = temp_y_start + parcels_side_y_sizes[i]
            parcel_x_size = random.triangular(
                const.min_joint_house_size,
                min(parcels_side_y_starts[i] - self.parcels_y_start,
                    self.parcels_y_start + self.parcels_y_size \
                        - (parcels_side_y_starts[i] +
                            parcels_side_y_sizes[i]),
                    self.parcels_x_size/2,
                    const.max_joint_house_depth))
            parcel.Parcel(self.parcels_x_start,
                          parcel_x_size,
                          parcels_side_y_starts[i],
                          parcels_side_y_sizes[i], 3, self,
                          "joint_house_side")
