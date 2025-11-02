.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

MechJeb service
===============


.. module:: MechJeb

This service provides functionality to interact with `MechJeb 2 <https://github.com/MuMech/MechJeb2>`_.


.. attribute:: api_ready

   A value indicating whether the service is available.

   :Attribute: Read-only, cannot be set
   :rtype: bool
   :Game Scenes: Flight





.. attribute:: airplane_autopilot



   :Attribute: Read-only, cannot be set
   :rtype: :class:`AirplaneAutopilot`
   :Game Scenes: Flight





.. attribute:: antenna_controller



   :Attribute: Read-only, cannot be set
   :rtype: :class:`DeployableController`
   :Game Scenes: Flight





.. attribute:: ascent_autopilot



   :Attribute: Read-only, cannot be set
   :rtype: :class:`AscentAutopilot`
   :Game Scenes: Flight





.. attribute:: docking_autopilot



   :Attribute: Read-only, cannot be set
   :rtype: :class:`DockingAutopilot`
   :Game Scenes: Flight





.. attribute:: landing_autopilot



   :Attribute: Read-only, cannot be set
   :rtype: :class:`LandingAutopilot`
   :Game Scenes: Flight





.. attribute:: maneuver_planner



   :Attribute: Read-only, cannot be set
   :rtype: :class:`ManeuverPlanner`
   :Game Scenes: Flight





.. attribute:: node_executor



   :Attribute: Read-only, cannot be set
   :rtype: :class:`NodeExecutor`
   :Game Scenes: Flight





.. attribute:: rcs_controller



   :Attribute: Read-only, cannot be set
   :rtype: :class:`RCSController`
   :Game Scenes: Flight





.. attribute:: rendezvous_autopilot



   :Attribute: Read-only, cannot be set
   :rtype: :class:`RendezvousAutopilot`
   :Game Scenes: Flight





.. attribute:: smart_ass



   :Attribute: Read-only, cannot be set
   :rtype: :class:`SmartASS`
   :Game Scenes: Flight





.. attribute:: smart_rcs



   :Attribute: Read-only, cannot be set
   :rtype: :class:`SmartRCS`
   :Game Scenes: Flight





.. attribute:: solar_panel_controller



   :Attribute: Read-only, cannot be set
   :rtype: :class:`DeployableController`
   :Game Scenes: Flight





.. attribute:: staging_controller



   :Attribute: Read-only, cannot be set
   :rtype: :class:`StagingController`
   :Game Scenes: Flight





.. attribute:: target_controller



   :Attribute: Read-only, cannot be set
   :rtype: :class:`TargetController`
   :Game Scenes: Flight





.. attribute:: thrust_controller



   :Attribute: Read-only, cannot be set
   :rtype: :class:`ThrustController`
   :Game Scenes: Flight





.. attribute:: translatron



   :Attribute: Read-only, cannot be set
   :rtype: :class:`Translatron`
   :Game Scenes: Flight


.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

AscentAutopilot
===============


.. class:: AscentAutopilot

   This module controls the Ascent Guidance in MechJeb 2.

   .. note::

      See `MechJeb2 wiki <https://github.com/MuMech/MechJeb2/wiki/Ascent-Guidance#initial-pitch-over-issues>`_ for more guidance on how to optimally set up this autopilot.

   .. attribute:: enabled



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: status

      The autopilot status; it depends on the selected ascent path.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. attribute:: ascent_path_index

      The selected ascent path.

      0 = :class:`AscentClassic` (Classic Ascent Profile)

      1 = :class:`AscentGT` (Stock-style GravityTurn)

      2 = :class:`AscentPVG` (Primer Vector Guidance (RSS/RO))

      :Attribute: Can be read or written
      :rtype: int
      :Game Scenes: Flight

   .. attribute:: ascent_path_classic

      Get Classic Ascent Profile settings.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`AscentClassic`
      :Game Scenes: Flight

   .. attribute:: ascent_path_gt

      Get Stock-style GravityTurn profile settings.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`AscentGT`
      :Game Scenes: Flight

   .. attribute:: ascent_path_pvg

      Get Powered Explicit Guidance (RSS/RO) profile settings.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`AscentPVG`
      :Game Scenes: Flight

   .. attribute:: desired_inclination

      The desired inclination in degrees for the final circular orbit.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: desired_orbit_altitude

      The desired altitude in meters for the final circular orbit.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: thrust_controller



      :Attribute: Read-only, cannot be set
      :rtype: :class:`ThrustController`
      :Game Scenes: Flight


      .. note::

         Equivalent to :attr:`thrust_controller`.

   .. attribute:: force_roll

      The state of force roll.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: turn_roll

      The turn roll used by the autopilot.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: vertical_roll

      The vertical/climb roll used by the autopilot.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: limit_ao_a

      Whether to limit angle of attack.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: max_ao_a

      The maximal angle of attack used by the autopilot.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: ao_a_limit_fadeout_pressure

      The pressure value when AoA limit is automatically deactivated.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: corrective_steering

      Will cause the craft to steer based on the more accurate velocity vector rather than positional vector (large craft may actually perform better with this box unchecked).

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: corrective_steering_gain

      The gain of corrective steering used by the autopilot.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: autostage

      The autopilot will automatically stage when the current stage has run out of fuel.
      Paramethers can be set in :class:`StagingController`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: staging_controller



      :Attribute: Read-only, cannot be set
      :rtype: :class:`StagingController`
      :Game Scenes: Flight


      .. note::

         Equivalent to :attr:`staging_controller`.

   .. attribute:: autodeploy_solar_panels

      Whether to deploy solar panels automatically when the ascent finishes.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: auto_deploy_antennas

      Whether to deploy antennas automatically when the ascent finishes.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: skip_circularization

      Whether to skip circularization burn and do only the ascent.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: warp_count_down



      :Attribute: Can be read or written
      :rtype: int
      :Game Scenes: Flight

   .. attribute:: launch_lan_difference



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: launch_phase_angle



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: launch_mode

      Current autopilot mode. Useful for determining whether the autopilot is performing a timed launch or not.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`AscentLaunchMode`
      :Game Scenes: Flight

   .. method:: abort_timed_launch()

      Abort a known timed launch when it has not started yet

      :Game Scenes: Flight

   .. method:: launch_to_rendezvous()

      Launch to rendezvous with the selected target.

      :Game Scenes: Flight

   .. method:: launch_to_target_plane()

      Launch into the plane of the selected target.

      :Game Scenes: Flight



.. class:: AscentLaunchMode




   .. data:: normal

      The autopilot is not performing a timed launch.


   .. data:: rendezvous

      The autopilot is performing a timed launch to rendezvous with the target vessel.


   .. data:: target_plane

      The autopilot is performing a timed launch to target plane.


   .. data:: unknown

      The autopilot is performing an unknown timed launch.



AscentClassic
-------------


.. class:: AscentClassic

   The Classic Ascent Profile.

   .. attribute:: auto_path

      Whether to enable automatic altitude turn.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: auto_turn_percent

      A value between 0 and 1.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: auto_turn_speed_factor

      A value between 0 and 1.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: auto_turn_start_altitude



      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: auto_turn_start_velocity



      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: auto_turn_end_altitude



      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: turn_start_altitude

      The turn starts when this altitude is reached.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: turn_start_velocity

      The turn starts when this velocity is reached.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: turn_end_altitude

      The turn ends when this altitude is reached.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: turn_end_angle

      The final flight path angle.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: turn_shape_exponent

      A value between 0 - 1 describing how steep the turn is.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight



AscentGT
--------


.. class:: AscentGT

   This profile is similar to the gravity turn mod. It is a 3-burn to orbit style of launch that can get to orbit with about 2800 dV on stock Kerbin.
   If you want to have fun make a rocket that is basically a nose cone, a jumbo-64 a mainsail and some fairly big fins, have the pitch program flip it over aggressively (uncheck the AoA limiter, set the values to like 0.5 / 50 / 40 / 45 / 1) and let it rip.

   .. note::

      It's not precisely the GT mod algorithm and it does not do any pitch-up during the intermediate burn right now, so it won't handle low TWR upper stages.

   .. attribute:: hold_ap_time

      At the intermediate altitude with this much time-to-apoapsis left the engine will start burning prograde to lift the apoapsis.
      The engine will throttle down in order to burn closer to the apoapsis.
      This is very similar to the lead-time of a maneuver node in concept, but with throttling down in the case where the player has initiated the burn too early (the corollary is that if you see lots of throttling down at the start, you likely need less HoldAP time).

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: intermediate_altitude

      Intermediate apoapsis altitude to coast to and then raise the apoapsis up to the eventual final target. May be set to equal the final target in order to skip the intermediate phase.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: turn_start_altitude

      Altitude in km to pitch over and initiate the Gravity Turn (higher values for lower-TWR rockets).

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: turn_start_pitch

      Pitch that the pitch program immediately applies.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: turn_start_velocity

      Velocity in m/s which triggers pitch over and initiates the Gravity Turn (higher values for lower-TWR rockets).

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight



AscentPVG
---------


.. class:: AscentPVG

   The Primer Vector Guidance (RSS/RO) profile.

   .. attribute:: attach_alt_flag



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: desired_apoapsis

      The target apoapsis in meters.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: desired_attach_alt



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: dynamic_pressure_trigger



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: fixed_coast



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: fixed_coast_length



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: pitch_rate



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: pitch_start_velocity



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: staging_trigger



      :Attribute: Can be read or written
      :rtype: int
      :Game Scenes: Flight

   .. attribute:: staging_trigger_flag



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

DockingAutopilot
================


.. class:: DockingAutopilot



   .. attribute:: enabled



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: status



      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. attribute:: speed_limit



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: override_safe_distance



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: overriden_safe_distance



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: override_target_size



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: overriden_target_size



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: safe_distance



      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: target_size



      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: force_roll



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: roll



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

LandingAutopilot
================


.. class:: LandingAutopilot

   The Landing Guidance module provides targeted and non-targeted landing autopilot.

   .. attribute:: enabled



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: status



      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. attribute:: deploy_chutes



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: deploy_gears



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. method:: land_at_position_target()



      :Game Scenes: Flight

   .. method:: land_untargeted()



      :Game Scenes: Flight

   .. attribute:: limit_chutes_stage



      :Attribute: Can be read or written
      :rtype: int
      :Game Scenes: Flight

   .. attribute:: limit_gears_stage



      :Attribute: Can be read or written
      :rtype: int
      :Game Scenes: Flight

   .. attribute:: rcs_adjustment



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. method:: stop_landing()



      :Game Scenes: Flight

   .. attribute:: touchdown_speed



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

RendezvousAutopilot
===================


.. class:: RendezvousAutopilot



   .. attribute:: enabled



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: status



      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. attribute:: desired_distance



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: max_phasing_orbits



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

.. class:: MJServiceException

   General exception for errors in the service.

.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

ManeuverPlanner
===============


.. class:: ManeuverPlanner



   .. attribute:: operation_apoapsis



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationApoapsis`
      :Game Scenes: Flight

   .. attribute:: operation_circularize



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationCircularize`
      :Game Scenes: Flight

   .. attribute:: operation_course_correction



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationCourseCorrection`
      :Game Scenes: Flight

   .. attribute:: operation_ellipticize



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationEllipticize`
      :Game Scenes: Flight

   .. attribute:: operation_inclination



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationInclination`
      :Game Scenes: Flight

   .. attribute:: operation_interplanetary_transfer



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationInterplanetaryTransfer`
      :Game Scenes: Flight

   .. attribute:: operation_kill_rel_vel



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationKillRelVel`
      :Game Scenes: Flight

   .. attribute:: operation_lambert



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationLambert`
      :Game Scenes: Flight

   .. attribute:: operation_lan



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationLan`
      :Game Scenes: Flight

   .. attribute:: operation_longitude



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationLongitude`
      :Game Scenes: Flight

   .. attribute:: operation_moon_return



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationMoonReturn`
      :Game Scenes: Flight

   .. attribute:: operation_periapsis



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationPeriapsis`
      :Game Scenes: Flight

   .. attribute:: operation_plane



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationPlane`
      :Game Scenes: Flight

   .. attribute:: operation_resonant_orbit



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationResonantOrbit`
      :Game Scenes: Flight

   .. attribute:: operation_semi_major



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationSemiMajor`
      :Game Scenes: Flight

   .. attribute:: operation_transfer



      :Attribute: Read-only, cannot be set
      :rtype: :class:`OperationTransfer`
      :Game Scenes: Flight



.. class:: OperationException

   This exception is thrown when there is something wrong with the operation (e.g. the target is not set when the operation needs it).



TimeSelector
------------


.. class:: TimeSelector



   .. attribute:: circularize_altitude

      To be used with :attr:`TimeReference.altitude`.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: lead_time

      To be used with :attr:`TimeReference.x_from_now`.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: time_reference



      :Attribute: Can be read or written
      :rtype: :class:`TimeReference`
      :Game Scenes: Flight



.. class:: TimeReference

   **IMPORTANT**: `TimeReference` is an enum accessed from the `mj` object, NOT from `maneuver_planner`.


   .. data:: altitude

      At the selected :attr:`TimeSelector.circularize_altitude`.


   .. data:: apoapsis

      At the next apoapsis.


   .. data:: closest_approach

      At the closest approach to the target.


   .. data:: computed

      At the optimum time.


   .. data:: eq_ascending

      At the equatorial ascending node.


   .. data:: eq_descending

      At the equatorial descending node.


   .. data:: eq_highest_ad

      At the cheapest equatorial AN/DN.


   .. data:: eq_nearest_ad

      At the nearest equatorial AN/DN.


   .. data:: periapsis

      At the next periapsis.


   .. data:: rel_ascending

      At the next ascending node with the target.


   .. data:: rel_descending

      At the next descending node with the target.


   .. data:: rel_highest_ad

      At the cheapest AN/DN with the target.


   .. data:: rel_nearest_ad

      At the nearest AN/DN with the target.


   .. data:: x_from_now

      After a fixed :attr:`TimeSelector.lead_time`.



Operations
----------

OperationApoapsis
^^^^^^^^^^^^^^^^^


.. class:: OperationApoapsis

   Create a maneuver to set a new apoapsis

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: new_apoapsis



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: time_selector



      :Attribute: Read-only, cannot be set
      :rtype: :class:`TimeSelector`
      :Game Scenes: Flight



OperationCircularize
^^^^^^^^^^^^^^^^^^^^


.. class:: OperationCircularize

   This mode creates a manevuer to match your apoapsis to periapsis.
   To match apoapsis to periapsis, set the time to :attr:`TimeReference.periapsis`; to match periapsis to apoapsis, set the time to :attr:`TimeReference.apoapsis`. These are the most efficient, but it can also create node at specific height or after specific time.

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: time_selector



      :Attribute: Read-only, cannot be set
      :rtype: :class:`TimeSelector`
      :Game Scenes: Flight



OperationCourseCorrection
^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: OperationCourseCorrection

   Create a maneuver to fine-tune closest approach to target

   .. attribute:: course_correct_final_pe_a



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. attribute:: intercept_distance



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight



OperationEllipticize
^^^^^^^^^^^^^^^^^^^^


.. class:: OperationEllipticize

   Create a maneuver to change both periapsis and apoapsis

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: new_apoapsis



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: new_periapsis



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: time_selector



      :Attribute: Read-only, cannot be set
      :rtype: :class:`TimeSelector`
      :Game Scenes: Flight



OperationInclination
^^^^^^^^^^^^^^^^^^^^


.. class:: OperationInclination

   Create a maneuver to change inclination

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: new_inclination



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: time_selector



      :Attribute: Read-only, cannot be set
      :rtype: :class:`TimeSelector`
      :Game Scenes: Flight



OperationInterplanetaryTransfer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: OperationInterplanetaryTransfer

   Create a maneuver to transfer to another planet

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: wait_for_phase_angle



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight



OperationKillRelVel
^^^^^^^^^^^^^^^^^^^


.. class:: OperationKillRelVel

   Match velocities with target

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: time_selector



      :Attribute: Read-only, cannot be set
      :rtype: :class:`TimeSelector`
      :Game Scenes: Flight



OperationLambert
^^^^^^^^^^^^^^^^


.. class:: OperationLambert

   Create a maneuver to set the chosen time

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. attribute:: intercept_interval



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: time_selector



      :Attribute: Read-only, cannot be set
      :rtype: :class:`TimeSelector`
      :Game Scenes: Flight



OperationLan
^^^^^^^^^^^^


.. class:: OperationLan

   Change longitude of ascending node

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: new_lan



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: time_selector



      :Attribute: Read-only, cannot be set
      :rtype: :class:`TimeSelector`
      :Game Scenes: Flight



OperationLongitude
^^^^^^^^^^^^^^^^^^


.. class:: OperationLongitude

   Change surface longitude of apsis

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: new_surface_longitude



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: time_selector



      :Attribute: Read-only, cannot be set
      :rtype: :class:`TimeSelector`
      :Game Scenes: Flight



OperationMoonReturn
^^^^^^^^^^^^^^^^^^^


.. class:: OperationMoonReturn

   Create a maneuver to return from a moon approximately at the specified altitude

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: moon_return_altitude

      Approximate return altitude from a moon (from an orbiting body to the parent body).

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight



OperationPeriapsis
^^^^^^^^^^^^^^^^^^


.. class:: OperationPeriapsis

   Create a maneuver to set a new periapsis

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: new_periapsis



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: time_selector



      :Attribute: Read-only, cannot be set
      :rtype: :class:`TimeSelector`
      :Game Scenes: Flight



OperationPlane
^^^^^^^^^^^^^^


.. class:: OperationPlane

   Create a maneuver to match planes with target

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: time_selector



      :Attribute: Read-only, cannot be set
      :rtype: :class:`TimeSelector`
      :Game Scenes: Flight



OperationResonantOrbit
^^^^^^^^^^^^^^^^^^^^^^


.. class:: OperationResonantOrbit

   Resonant orbit is useful for placing satellites to a constellation. This mode should be used starting from a orbit in the desired orbital plane. Important parameter to this mode is the desired orbital ratio, which is the ratio between period of your current orbit and the new orbit.
   To deploy satellites, set the denominator to number of satellites you want to have in the constellation. Setting the nominator to one less than denominator is the most efficient, but not necessary the fastest. To successfully deploy all satellites, make sure the numbers are incommensurable.

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: resonance_denominator



      :Attribute: Can be read or written
      :rtype: int
      :Game Scenes: Flight

   .. attribute:: resonance_numerator



      :Attribute: Can be read or written
      :rtype: int
      :Game Scenes: Flight

   .. attribute:: time_selector



      :Attribute: Read-only, cannot be set
      :rtype: :class:`TimeSelector`
      :Game Scenes: Flight



OperationSemiMajor
^^^^^^^^^^^^^^^^^^


.. class:: OperationSemiMajor

   Create a maneuver to set a new semi-major axis

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: new_semi_major_axis



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: time_selector



      :Attribute: Read-only, cannot be set
      :rtype: :class:`TimeSelector`
      :Game Scenes: Flight



OperationTransfer
^^^^^^^^^^^^^^^^^


.. class:: OperationTransfer

   Bi-impulsive (Hohmann) transfer to target.

   This option is used to plan transfer to target in single sphere of influence. It is suitable for rendezvous with other vessels or moons.
   Contrary to the name, the transfer is often uni-impulsive. You can select when you want the manevuer to happen or select optimum time.

   .. attribute:: error_message

      A warning may be stored there during MakeNode() call.

      :Attribute: Read-only, cannot be set
      :rtype: str
      :Game Scenes: Flight

   .. method:: make_node()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: The first maneuver node necessary to perform this operation.
      :rtype: :class:`SpaceCenter.Node`
      :Game Scenes: Flight


      .. note::

         This method is deprecated, use MakeNodes instead.

   .. method:: make_nodes()

      Execute the operation and create appropriate maneuver nodes.
      A warning may be stored in ErrorMessage during this process; so it may be useful to check its value.

      OperationException is thrown when there is something wrong with the operation.
      MJServiceException - Internal service error.

      :returns: A list of maneuver nodes necessary to perform this operation
      :rtype: list(:class:`SpaceCenter.Node`)
      :Game Scenes: Flight

   .. attribute:: intercept_only

      Intercept only, no capture burn (impact/flyby)

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: period_offset

      Fractional target period offset

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: simple_transfer

      Simple coplanar Hohmann transfer.
      Set it to true if you are used to the old version of transfer maneuver.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight


      .. note::

         If set to true, TimeSelector property is ignored.

   .. attribute:: time_selector



      :Attribute: Read-only, cannot be set
      :rtype: :class:`TimeSelector`
      :Game Scenes: Flight

.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

SmartASS
========


.. class:: SmartASS

   The Smart A.S.S. module provides aids for vessel pitch control.

   .. attribute:: interface_mode

      GUI mode; doesn't do anything except changing SmartASS GUI buttons to a specified mode.

      :Attribute: Can be read or written
      :rtype: :class:`SmartASSInterfaceMode`
      :Game Scenes: Flight

   .. attribute:: autopilot_mode

      Current autopilot mode.

      :Attribute: Can be read or written
      :rtype: :class:`SmartASSAutopilotMode`
      :Game Scenes: Flight

   .. method:: update(reset_pid)

      Update SmartASS position to use new values.

      :param bool reset_pid: False most of the time, use true only if it doesn't work.
      :Game Scenes: Flight

   .. attribute:: force_yaw

      Enable yaw control for :attr:`SmartASS.surface_heading`, :attr:`SmartASSAutopilotMode.surface_prograde` and :attr:`SmartASSAutopilotMode.surface_retrograde`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: force_pitch

      Enable pitch control for :attr:`SmartASS.surface_pitch`, :attr:`SmartASSAutopilotMode.surface_prograde` and :attr:`SmartASSAutopilotMode.surface_retrograde`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: force_roll

      Enable roll control.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: surface_heading

      Heading; Also called or azimuth, or the direction where you want to go.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight


      .. note::

         Works only in :attr:`SmartASSAutopilotMode.surface` mode.

   .. attribute:: surface_pitch

      Pitch or inclination; 0 is horizontal and 90 is straight up. Can be negative.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight


      .. note::

         Works only in :attr:`SmartASSAutopilotMode.surface` mode.

   .. attribute:: surface_roll

      Roll; 0 is top side up.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight


      .. note::

         Works only in :attr:`SmartASSAutopilotMode.surface` mode.

   .. attribute:: surface_vel_yaw



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight


      .. note::

         Works only in :attr:`SmartASSAutopilotMode.surface_prograde` and :attr:`SmartASSAutopilotMode.surface_retrograde` mode.

   .. attribute:: surface_vel_pitch

      Pitch or inclination; 0 is horizontal and 90 is straight up. Can be negative.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight


      .. note::

         Works only in :attr:`SmartASSAutopilotMode.surface_prograde` and :attr:`SmartASSAutopilotMode.surface_retrograde` mode.

   .. attribute:: surface_vel_roll

      Roll; 0 is top side up.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight


      .. note::

         Works only in :attr:`SmartASSAutopilotMode.surface_prograde` and :attr:`SmartASSAutopilotMode.surface_retrograde` mode.

   .. attribute:: advanced_reference



      :Attribute: Can be read or written
      :rtype: :class:`AttitudeReference`
      :Game Scenes: Flight


      .. note::

         Works only in :attr:`SmartASSAutopilotMode.advanced` mode.

   .. attribute:: advanced_direction



      :Attribute: Can be read or written
      :rtype: :class:`Direction`
      :Game Scenes: Flight


      .. note::

         Works only in :attr:`SmartASSAutopilotMode.advanced` mode.



.. class:: SmartASSInterfaceMode




   .. data:: orbital




   .. data:: surface




   .. data:: target




   .. data:: advanced




   .. data:: automatic

      Internal mode, do not set.



.. class:: SmartASSAutopilotMode




   .. data:: off

      Switch off Smart A.S.S.


   .. data:: kill_rot

      "Kill" the spacecraft's rotation (counters rotation/tumbling).


   .. data:: node

      Point the vessel to a maneuver node.


   .. data:: advanced

      Advanced mode.


   .. data:: automatic

      Automatic mode (internal mode, only for getting status).


   .. data:: prograde

      ORBIT: Orient to orbital prograde.


   .. data:: retrograde

      ORBIT: Orient to orbital retrograde.


   .. data:: normal_plus

      ORBIT: Orient to orbital normal (change inclination).


   .. data:: normal_minus

      ORBIT: Orient to orbital anti-normal (change inclination).


   .. data:: radial_plus

      ORBIT: Orient to radial outward (away from SOI).


   .. data:: radial_minus

      ORBIT: Orient to radial inward (towards SOI).


   .. data:: surface_prograde

      SURFACE: Orient in the direction of movement relative to the ground. Useful during lift-off for rockets which don't have fins or are otherwise instable.


   .. data:: surface_retrograde

      SURFACE: Orient in the opposite direction of movement relative to the ground. Useful during reentry or aerobraking with an aerodynamically unstable craft.


   .. data:: horizontal_plus

      SURFACE: Orient in the direction of horizontal movement relative to the ground.


   .. data:: horizontal_minus

      SURFACE: Orient in the opposite direction of horizontal movement relative to the ground.


   .. data:: surface

      SURFACE: Orient the vessel in specific direction relative to surface.


   .. data:: vertical_plus

      SURFACE: Orient "up", perpendicular to the surface.


   .. data:: target_plus

      TARGET: Orient towards the target.


   .. data:: target_minus

      TARGET: Orient away from the target.


   .. data:: relative_plus

      TARGET: Orient toward your relative velocity. Burning this direction will increase your relative velocity.


   .. data:: relative_minus

      TARGET: Orient away from your relative velocity. Burning this direction will decrease your relative velocity.


   .. data:: parallel_plus

      TARGET: Orient parallel to the target's orientation. If the target is a docking node it orients the ship along the docking axis, pointing away from the node.


   .. data:: parallel_minus

      TARGET: Orient antiparallel to the target's orientation. If the target is a docking node it orients the ship along the docking axis, pointing toward the node.



.. class:: AttitudeReference




   .. data:: inertial

      World coordinate system.


   .. data:: orbit

      forward = prograde, left = normal plus, up = radial plus


   .. data:: orbit_horizontal

      forward = surface projection of orbit velocity, up = surface normal


   .. data:: surface_north

      forward = north, left = west, up = surface normal


   .. data:: surface_velocity

      forward = surface frame vessel velocity, up = perpendicular component of surface normal


   .. data:: target

      forward = toward target, up = perpendicular component of vessel heading


   .. data:: relative_velocity

      forward = toward relative velocity direction, up = tbd


   .. data:: target_orientation

      forward = direction target is facing, up = target up


   .. data:: maneuver_node

      forward = next maneuver node direction, up = tbd


   .. data:: sun

      forward = orbit velocity of the parent body orbiting the sun, up = radial plus of that orbit


   .. data:: surface_horizontal

      forward = surface velocity horizontal component, up = surface normal



.. class:: Direction




   .. data:: forward




   .. data:: back




   .. data:: up




   .. data:: down




   .. data:: right




   .. data:: left

.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

SmartRCS
========


.. class:: SmartRCS



   .. attribute:: auto_disable_smart_rcs



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: mode



      :Attribute: Can be read or written
      :rtype: :class:`SmartRCSMode`
      :Game Scenes: Flight

   .. attribute:: rcs_controller



      :Attribute: Read-only, cannot be set
      :rtype: :class:`RCSController`
      :Game Scenes: Flight



.. class:: SmartRCSMode




   .. data:: off




   .. data:: zero_relative_velocity




   .. data:: zero_velocity

.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

Translatron
===========


.. class:: Translatron

   The Translatron module controls the vessel's throttle/velocity.

   .. attribute:: mode

      Current translatron mode.

      :Attribute: Can be read or written
      :rtype: :class:`TranslatronMode`
      :Game Scenes: Flight

   .. attribute:: translation_speed

      Speed which trasnlatron will hold

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: kill_horizontal_speed

      Kill horizontal speed

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. method:: panic_switch()

      Abort mission by seperating all but the last stage and activating landing autopilot.

      :Game Scenes: Flight



.. class:: TranslatronMode




   .. data:: off

      Switch off Translatron.


   .. data:: keep_orbital

      Keep orbital velocity.


   .. data:: keep_surface

      Keep surface velocity.


   .. data:: keep_vertical

      Keep vertical velocity (climb/descent speed).


   .. data:: keep_relative

      Internal mode, do not set.


   .. data:: direct

      Internal mode, do not set.

.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

DeployableController
====================


.. class:: DeployableController



   .. method:: all_retracted()

      Check if all deployable modules of this type are retracted.

      :returns: True if all modules are retracted; False otherwise
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: auto_deploy

      Automatically deploy modules of this type when controlled by a MechJeb autopilot

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. method:: extend_all()

      Extend all deployable modules of this type.

      :Game Scenes: Flight

   .. method:: retract_all()

      Retract all deployable modules of this type.

      :Game Scenes: Flight

.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

NodeExecutor
============


.. class:: NodeExecutor



   .. attribute:: enabled



      :Attribute: Read-only, cannot be set
      :rtype: bool
      :Game Scenes: Flight

   .. method:: abort()



      :Game Scenes: Flight

   .. attribute:: autowarp



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. method:: execute_all_nodes()



      :Game Scenes: Flight

   .. method:: execute_one_node()



      :Game Scenes: Flight

   .. attribute:: lead_time



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: tolerance



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

RCSController
=============


.. class:: RCSController



   .. attribute:: rcs_for_rotation



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: rcs_throttle



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

StagingController
=================


.. class:: StagingController



   .. attribute:: enabled



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: autostaging_once

      The autostaging mode. If set to true, it will automatically disable itself after one staging action.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight


      .. note::

         The controller needs to be enabled for this to work.

   .. attribute:: autostage_limit

      Stop at the selected stage - staging will not occur beyond this stage number.

      :Attribute: Can be read or written
      :rtype: int
      :Game Scenes: Flight

   .. attribute:: autostage_post_delay

      The autopilot will pause the actual staging after ? seconds for each stage.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: autostage_pre_delay

      The autopilot will pause the actual staging before ? seconds for each stage.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: clamp_auto_stage_thrust_pct



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: fairing_max_aerothermal_flux



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: fairing_max_dynamic_pressure



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: fairing_min_altitude



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: hot_staging



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: hot_staging_lead_time



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

TargetController
================


.. class:: TargetController



   .. attribute:: can_align



      :Attribute: Read-only, cannot be set
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: distance



      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: docking_axis



      :Attribute: Read-only, cannot be set
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. method:: get_position_target_position()



      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. method:: get_position_target_string()



      :rtype: str
      :Game Scenes: Flight

   .. attribute:: normal_target_exists



      :Attribute: Read-only, cannot be set
      :rtype: bool
      :Game Scenes: Flight

   .. method:: pick_position_target_on_map()



      :Game Scenes: Flight

   .. attribute:: position



      :Attribute: Read-only, cannot be set
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: position_target_exists



      :Attribute: Read-only, cannot be set
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: relative_position



      :Attribute: Read-only, cannot be set
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: relative_velocity



      :Attribute: Read-only, cannot be set
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. method:: set_direction_target(name)



      :param str name:
      :Game Scenes: Flight

   .. method:: set_position_target(body, latitude, longitude)



      :param SpaceCenter.CelestialBody body:
      :param float latitude:
      :param float longitude:
      :Game Scenes: Flight

   .. attribute:: target_orbit



      :Attribute: Read-only, cannot be set
      :rtype: :class:`SpaceCenter.Orbit`
      :Game Scenes: Flight

   .. method:: update_direction_target(direction)



      :param tuple direction:
      :Game Scenes: Flight

.. default-domain:: py
.. highlight:: py
.. currentmodule:: MechJeb

ThrustController
================


.. class:: ThrustController



   .. attribute:: differential_throttle



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: differential_throttle_status



      :Attribute: Read-only, cannot be set
      :rtype: :class:`DifferentialThrottleStatus`
      :Game Scenes: Flight

   .. attribute:: electric_throttle



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: electric_throttle_hi



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: electric_throttle_lo



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: flameout_safety_pct

      The jet safety margin. A value between 0 and 1.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: limit_acceleration



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: limit_dynamic_pressure



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: limit_throttle



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: limit_to_prevent_flameout



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: limit_to_prevent_overheats

      Limits the throttle to prevent parts from overheating.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: limiter_min_throttle



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: manage_intakes



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: max_acceleration

      Limit acceleration to [m/s^2] (never exceed the acceleration during ascent).

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: max_dynamic_pressure

      Limit the maximal dynamic pressure in Pa.
      This avoids that pieces break off during launch because of atmospheric pressure.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: max_throttle

      Never exceed the percentage of the throttle during ascent (value between 0 and 1).

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: min_throttle

      Never go below the percentage of the throttle during ascent (value between 0 and 1).

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: smooth_throttle



      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: throttle_smoothing_time



      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight



.. class:: DifferentialThrottleStatus




   .. data:: all_engines_off




   .. data:: more_engines_required




   .. data:: solver_failed




   .. data:: success