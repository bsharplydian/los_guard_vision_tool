import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.widgets import Slider, TextBox

fig = plt.figure(figsize=(10, 8), layout='constrained')

gs = fig.add_gridspec(2, 1, height_ratios=[1, 0.5], hspace=0.4)
gs_plots = gs[0].subgridspec(2, 4)
gs_sliders = gs[1].subgridspec(10, 3, width_ratios=[0.3, 1, 0.3])

stationary_plot = fig.add_subplot(gs_plots[0, 0], projection='polar')
ax_stationary = fig.add_subplot(gs_plots[1, 0])

crouched_plot = fig.add_subplot(gs_plots[0, 1], projection='polar')
ax_crouched = fig.add_subplot(gs_plots[1, 1])

walking_plot = fig.add_subplot(gs_plots[0, 2], projection='polar')
ax_walking = fig.add_subplot(gs_plots[1, 2])

sprinting_plot = fig.add_subplot(gs_plots[0, 3], projection='polar')
ax_sprinting = fig.add_subplot(gs_plots[1, 3])


ax_distance_w_y = fig.add_subplot(gs_sliders[0, 1])
ax_angle_w_y = fig.add_subplot(gs_sliders[1, 1])
ax_light_w_y = fig.add_subplot(gs_sliders[2, 1])
ax_distance_w_r = fig.add_subplot(gs_sliders[3, 1])
ax_angle_w_r = fig.add_subplot(gs_sliders[4, 1])
ax_light_w_r = fig.add_subplot(gs_sliders[5, 1])
ax_yellow_t = fig.add_subplot(gs_sliders[6, 1])
ax_red_t = fig.add_subplot(gs_sliders[7, 1])
ax_lose_sight_radius = fig.add_subplot(gs_sliders[8, 1])
ax_sight_radius = fig.add_subplot(gs_sliders[9, 1])

# USER INPUT
# player
stationary_light_amount = Slider(ax_stationary, 'Stationary Light', 0.0, 1.0, valinit=0.05, orientation='vertical')
# stationary_light_amount.label.set_position((0.5, 1.5))
crouched_light_amount = Slider(ax_crouched, 'Crouched Light', 0.0, 1.0, valinit=0.1, orientation='vertical')
# crouched_light_amount.label.set_position((0.5, 1.5))
walking_light_amount = Slider(ax_walking, 'Walking Light', 0.0, 1.0, valinit=0.5, orientation='vertical')
# walking_light_amount.label.set_position((0.5, 1.5))
sprinting_light_amount = Slider(ax_sprinting, 'Sprinting Light', 0.0, 1.0, valinit=0.8, orientation='vertical')
# sprinting_light_amount.label.set_position((0.5, 1.5))

# guard controller
distance_weight_y = Slider(ax_distance_w_y, 'Distance Weight (Yellow)', 0.0, 10.0, valinit=1.78)
angle_weight_y = Slider(ax_angle_w_y, 'Angle Weight (Yellow)', 0.0, 10.0, valinit=3.78)
light_weight_y = Slider(ax_light_w_y, 'Light Weight (Yellow)', 0.0, 10.0, valinit=6.42)

distance_weight_r = Slider(ax_distance_w_r, 'Distance Weight (Red)', 0.0, 10.0, valinit=2.38)
angle_weight_r = Slider(ax_angle_w_r, 'Angle Weight (Red)', 0.0, 10.0, valinit=1.77)
light_weight_r = Slider(ax_light_w_r, 'Light Weight (Red)', 0.0, 10.0, valinit=0.9)

yellow_threshold = Slider(ax_yellow_t, 'Yellow Threshold', 0.0, 1.0, valinit=0.4)
red_threshold = Slider(ax_red_t, 'Red Threshold', 0.0, 1.0, valinit=0.687)

# enemy perception
lose_sight_radius = Slider(ax_lose_sight_radius, 'Lose Sight Radius', 100, 4000, valinit=3500)
sight_radius = Slider(ax_sight_radius, 'Sight Radius', 100, 4000, valinit=3000)

theta=np.linspace(0, 2*np.pi, 400)

def plot_vision_cone(plot: Axes, light_amount: float,
                     n_angle_weight_y: float, n_distance_weight_y: float, n_light_weight_y: float,
                     n_angle_weight_r: float, n_distance_weight_r: float, n_light_weight_r: float):
    plot.clear()
    plot.set_theta_zero_location('N')
    plot.set_rticks([lose_sight_radius.val/10*i for i in range(10)])
    plot.set_rlim(bottom=0, top=lose_sight_radius.val)
    plot.set_thetamin(-90)
    plot.set_thetamax(90)
    r_yellow = lose_sight_radius.val*(1 + (n_angle_weight_y * np.cos(theta) + n_light_weight_y * light_amount - yellow_threshold.val) / n_distance_weight_y)
    r_red = lose_sight_radius.val*(1 + (n_angle_weight_r * np.cos(theta) + n_light_weight_r * light_amount - red_threshold.val) / n_distance_weight_r)
    plot.plot(theta, np.full_like(theta, lose_sight_radius.val), color='pink', linewidth=2)
    plot.plot(theta, np.full_like(theta, sight_radius.val), color='lime', linewidth=0.5)
    plot.plot(theta, r_yellow, color='orange', linewidth=2)
    plot.plot(theta, r_red, color='red', linewidth=2)
    plot.fill_between(theta, 0, r_red, alpha=0.2, color='red')
    plot.fill_between(theta, 0, r_yellow, alpha=0.2, color='yellow')

def normalize_weights(a: float, d: float, l: float) -> (float, float, float):
    t: float = a+d+l
    print(a, d, l, t)
    print(a/t, d/t, l/t)
    return a/t, d/t, l/t
def update(val):
    n_angle_weight_y, n_distance_weight_y, n_light_weight_y = normalize_weights(angle_weight_y.val, distance_weight_y.val, light_weight_y.val)
    n_angle_weight_r, n_distance_weight_r, n_light_weight_r = normalize_weights(angle_weight_r.val, distance_weight_r.val, light_weight_r.val)

    plot_vision_cone(stationary_plot, stationary_light_amount.val,
                     n_angle_weight_y, n_distance_weight_y, n_light_weight_y,
                     n_angle_weight_r, n_distance_weight_r, n_light_weight_r)
    plot_vision_cone(crouched_plot, crouched_light_amount.val,
                     n_angle_weight_y, n_distance_weight_y, n_light_weight_y,
                     n_angle_weight_r, n_distance_weight_r, n_light_weight_r)
    plot_vision_cone(walking_plot, walking_light_amount.val,
                     n_angle_weight_y, n_distance_weight_y, n_light_weight_y,
                     n_angle_weight_r, n_distance_weight_r, n_light_weight_r)
    plot_vision_cone(sprinting_plot, sprinting_light_amount.val,
                     n_angle_weight_y, n_distance_weight_y, n_light_weight_y,
                     n_angle_weight_r, n_distance_weight_r, n_light_weight_r)
    plt.show()

stationary_light_amount.on_changed(update)
crouched_light_amount.on_changed(update)
walking_light_amount.on_changed(update)
sprinting_light_amount.on_changed(update)
lose_sight_radius.on_changed(update)
sight_radius.on_changed(update)

angle_weight_y.on_changed(update)
distance_weight_y.on_changed(update)
light_weight_y.on_changed(update)
angle_weight_r.on_changed(update)
distance_weight_r.on_changed(update)
light_weight_r.on_changed(update)

yellow_threshold.on_changed(update)
red_threshold.on_changed(update)

update(0)

plt.show()