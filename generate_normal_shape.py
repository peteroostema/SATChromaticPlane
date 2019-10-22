import math

def generate_normal_shape(num_of_edge, edge_length, plane_size):
    shape_list = []
    if num_of_edge == 4:
        shape = [1,[0,0],[0,edge_length],[edge_length,0],[edge_length,edge_length]]
        shape_list.append(shape)
        col = math.floor(plane_size/edge_length)
        for i in range(col):
            new_shape = shape[:]
            new_shape[0] = new_shape[0] + 1
            for i in range(num_of_edge+1)[1:]:
                new_shape[i][0] = new_shape[i][0] + edge_length
            add_new = new_shape[:]
            shape_list.append(add_new)
            shape = add_new[:]
    return shape_list
