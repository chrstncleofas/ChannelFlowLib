import math

from .constants import GRAVITY_G


def solve_critical_flow_rectangular(flow_area: float,
                                    base_width: float,
                                    average_velocity: float,
                                    discharge: float,
                                    manning_roughness: float):
    hydraulic_depth = flow_area / base_width
    froude_number = average_velocity / math.sqrt(GRAVITY_G * hydraulic_depth)
    discharge_intensity = discharge / base_width
    critical_depth = math.pow(math.pow(discharge_intensity, 2.0) / GRAVITY_G, (1.0 / 3.0))
    critical_top_width = base_width
    critical_wetted_perimeter = base_width + (2 * critical_depth)
    critical_flow_area = base_width * critical_depth
    critical_hydraulic_radius = critical_flow_area / critical_wetted_perimeter
    critical_slope = GRAVITY_G * math.pow(manning_roughness, 2.0) * \
                     (critical_wetted_perimeter / critical_top_width) / \
                     math.pow(1, 2.0) * math.pow(critical_hydraulic_radius, (1.0/3.0))

    return {
        'hydraulic_depth': hydraulic_depth,
        'froude_number': froude_number,
        'discharge_intensity': discharge_intensity,
        'critical_depth': critical_depth,
        'critical_top_width': critical_top_width,
        'critical_wetted_perimeter': critical_wetted_perimeter,
        'critical_flow_area': critical_flow_area,
        'critical_hydraulic_radius': critical_hydraulic_radius,
        'critical_slope': critical_slope
    }


def solve_critical_flow_trapezoidal(discharge: float,
                                    water_depth: float,
                                    channel_base: float,
                                    side_slope: float,
                                    roughness: float,
                                    flow_area: float,
                                    velocity: float):

    Q2g = pow(discharge, 2.0) / GRAVITY_G

    tester = 0.0

    # Critical depth
    critical_depth = 0.0

    # Critical area, perimeter, hydraulic radius, critical slope
    critical_flow_area = 0.0

    while tester < Q2g:
        critical_depth += 0.00001
        top_width = channel_base + 2 * side_slope * critical_depth
        critical_flow_area = (top_width + channel_base) / 2 * critical_depth
        tester = pow(critical_flow_area, 3) / top_width

    critical_wetted_perimeter = 2 * critical_depth * math.sqrt(pow(side_slope, 2) + 1) + channel_base
    critical_hydraulic_radius = critical_flow_area / critical_wetted_perimeter
    critical_slope = pow(discharge / (critical_flow_area * pow(critical_hydraulic_radius, (2.0 / 3.0))) * roughness, 2.0)

    # Solve for froude number
    top_width = channel_base + 2 * side_slope * water_depth
    hydraulic_depth = flow_area / top_width
    froude_number = velocity / math.sqrt(GRAVITY_G * hydraulic_depth)

    discharge_intensity = discharge / top_width

    return {
        'hydraulic_depth': hydraulic_depth,
        'froude_number': froude_number,
        'discharge_intensity': discharge_intensity,
        'critical_depth': critical_depth,
        'top_width': top_width,
        'critical_wetted_perimeter': critical_wetted_perimeter,
        'critical_flow_area': critical_flow_area,
        'critical_hydraulic_radius': critical_hydraulic_radius,
        'critical_slope': critical_slope
    }
