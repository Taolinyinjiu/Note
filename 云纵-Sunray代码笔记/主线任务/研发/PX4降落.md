# Land Detector
Land Detector 指的是PX4内部的降落检测器，其一共有七个参数，分别是
- LNDMC_ALT_MAX     多旋翼最大高度限制
- LNDMC_FFALL_THR   自由落体加速度阈值
- LNDMC_FFALL_TTRI  自由落体触发时间
- LNDMC_ROT_MAX     最大旋转角速度
- LNDMC_THR_RANGE   油门范围缩放:只有当油门低于这个值时，且满足其他条件，系统才能判断为land模式
- LNDMC_XY_VEL_MAX  最大水平速度
- LNDMC_Z_VEL_MAX   最大垂直速度

## PX4着陆状态

PX4对飞行器的着陆与否有五种状态，它们分别是1、FREEFALL；2、LANDED；3、MAYBE_LANDED；4、GROUND_CONTACT；5、FLYING。这五种状态是互斥的，同一时间只能存在某一种状态。

/**
 * @file MulticopterLandDetector.cpp
 *
 *The MC land-detector goes through 3 states before it will detect landed:
 *
 *State 1 (=ground_contact):
 *ground_contact is detected once the vehicle is not moving along the NED-z direction and has
 *a thrust value below 0.3 of the thrust_range (thrust_hover - thrust_min). The condition has to be true
 *for GROUND_CONTACT_TRIGGER_TIME_US in order to detect ground_contact
 *
 *State 2 (=maybe_landed):
 *maybe_landed can only occur if the internal ground_contact hysteresis state is true. maybe_landed criteria requires to have no motion in x and y,
 *no rotation and a thrust below 0.1 of the thrust_range (thrust_hover - thrust_min). In addition, the mc_pos_control turns off the thrust_sp in
 *body frame along x and y which helps to detect maybe_landed. The criteria for maybe_landed needs to be true for (LNDMC_TRIG_TIME / 3) seconds.
 *
 *State 3 (=landed)
 *landed can only be detected if maybe_landed is true for LAND_DETECTOR_TRIGGER_TIME_US. No farther criteria is tested, but the mc_pos_control goes into
 *idle (thrust_sp = 0) which helps to detect landed. By doing this the thrust-criteria of State 2 will always be met, however the remaining criteria of no rotation and no motion still
 *have to be valid.

 *It is to note that if one criteria is not met, then vehicle exits the state directly without blocking.
 *
 *If the land-detector does not detect ground_contact, then the vehicle is either flying or falling, where free fall detection heavily relies
 *on the acceleration. TODO: verify that free fall is reliable
 *
 * @author Johan Jansen <jnsn.johan@gmail.com>
 * @author Morten Lysgaard <morten@lysgaard.no>
 * @author Julian Oes <julian@oes.ch>
 */


