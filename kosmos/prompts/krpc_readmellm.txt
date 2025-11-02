.. default-domain:: py
.. highlight:: py
.. currentmodule:: SpaceCenter

SpaceCenter
===========


.. module:: SpaceCenter

Provides functionality to interact with Kerbal Space Program. This includes controlling
the active vessel, managing its resources, planning maneuver nodes and auto-piloting.


.. attribute:: science

   The current amount of science.

   :Attribute: Read-only, cannot be set
   :rtype: float
   




.. attribute:: funds

   The current amount of funds.

   :Attribute: Read-only, cannot be set
   :rtype: float
   




.. attribute:: reputation

   The current amount of reputation.

   :Attribute: Read-only, cannot be set
   :rtype: float
   




.. attribute:: active_vessel

   The currently active vessel.

   :Attribute: Can be read or written
   :rtype: :class:`Vessel`
   




.. attribute:: vessels

   A list of all the vessels in the game.

   :Attribute: Read-only, cannot be set
   :rtype: list(:class:`Vessel`)
   




.. attribute:: launch_sites

   A list of available launch sites.

   :Attribute: Read-only, cannot be set
   :rtype: list(:class:`LaunchSite`)
   




.. attribute:: bodies

   A dictionary of all celestial bodies (planets, moons, etc.) in the game,
   keyed by the name of the body.

   :Attribute: Read-only, cannot be set
   :rtype: dict(str, :class:`CelestialBody`)
   




.. attribute:: target_body

   The currently targeted celestial body.

   :Attribute: Can be read or written
   :rtype: :class:`CelestialBody`
   :Game Scenes: Flight





.. attribute:: target_vessel

   The currently targeted vessel.

   :Attribute: Can be read or written
   :rtype: :class:`Vessel`
   :Game Scenes: Flight





.. attribute:: target_docking_port

   The currently targeted docking port.

   :Attribute: Can be read or written
   :rtype: :class:`DockingPort`
   :Game Scenes: Flight





.. staticmethod:: clear_target()

   Clears the current target.

   :Game Scenes: Flight





.. staticmethod:: launchable_vessels(craft_directory)

   Returns a list of vessels from the given *craft_directory*
   that can be launched.

   :param str craft_directory: Name of the directory in the current saves "Ships" directory. For example ``"VAB"`` or ``"SPH"``.
   :rtype: list(str)
   




.. staticmethod:: launch_vessel(craft_directory, name, launch_site, [recover = True], [crew = None], [flag_url = ''])

   Launch a vessel.

   :param str craft_directory: Name of the directory in the current saves "Ships" directory, that contains the craft file. For example ``"VAB"`` or ``"SPH"``.
   :param str name: Name of the vessel to launch. This is the name of the ".craft" file in the save directory, without the ".craft" file extension.
   :param str launch_site: Name of the launch site. For example ``"LaunchPad"`` or ``"Runway"``.
   :param bool recover: If true and there is a vessel on the launch site, recover it before launching.
   :param list crew: If not ``None``, a list of names of Kerbals to place in the craft. Otherwise the crew will use default assignments.
   :param str flag_url: If not ``None``, the asset URL of the mission flag to use for the launch.
   

   .. note::

      Throws an exception if any of the games pre-flight checks fail.




.. staticmethod:: launch_vessel_from_vab(name, [recover = True])

   Launch a new vessel from the VAB onto the launchpad.

   :param str name: Name of the vessel to launch.
   :param bool recover: If true and there is a vessel on the launch pad, recover it before launching.
   

   .. note::

      This is equivalent to calling :meth:`launch_vessel` with the craft directory
      set to "VAB" and the launch site set to "LaunchPad".
      Throws an exception if any of the games pre-flight checks fail.




.. staticmethod:: launch_vessel_from_sph(name, [recover = True])

   Launch a new vessel from the SPH onto the runway.

   :param str name: Name of the vessel to launch.
   :param bool recover: If true and there is a vessel on the runway, recover it before launching.
   

   .. note::

      This is equivalent to calling :meth:`launch_vessel` with the craft directory
      set to "SPH" and the launch site set to "Runway".
      Throws an exception if any of the games pre-flight checks fail.




.. staticmethod:: save(name)

   Save the game with a given name.
   This will create a save file called ``name.sfs`` in the folder of the
   current save game.

   :param str name: Name of the save.
   




.. staticmethod:: load(name)

   Load the game with the given name.
   This will create a load a save file called ``name.sfs`` from the folder of the
   current save game.

   :param str name: Name of the save.
   




.. staticmethod:: quicksave()

   Save a quicksave.

   

   .. note::

      This is the same as calling :meth:`save` with the name "quicksave".




.. staticmethod:: quickload()

   Load a quicksave.

   

   .. note::

      This is the same as calling :meth:`load` with the name "quicksave".




.. staticmethod:: can_revert_to_launch()

   Whether the current flight can be reverted to launch.

   :rtype: bool
   




.. staticmethod:: revert_to_launch()

   Revert the current flight to launch.

   




.. staticmethod:: transfer_crew(crew_member, target_part)

   Transfers a crew member to a different part.

   :param CrewMember crew_member: The crew member to transfer.
   :param Part target_part: The part to move them to.
   :Game Scenes: Flight





.. attribute:: ui_visible

   Whether the UI is visible.

   :Attribute: Can be read or written
   :rtype: bool
   :Game Scenes: Flight





.. attribute:: navball

   Whether the navball is visible.

   :Attribute: Can be read or written
   :rtype: bool
   :Game Scenes: Flight





.. attribute:: ut

   The current universal time in seconds.

   :Attribute: Read-only, cannot be set
   :rtype: float
   




.. attribute:: g

   The value of the `gravitational constant <https://en.wikipedia.org/wiki/Gravitational_constant>`_ G in :math:`N(m/kg)^2`.

   :Attribute: Read-only, cannot be set
   :rtype: float
   




.. attribute:: warp_rate

   The current warp rate. This is the rate at which time is passing for
   either on-rails or physical time warp. For example, a value of 10 means
   time is passing 10x faster than normal. Returns 1 if time warp is not
   active.

   :Attribute: Read-only, cannot be set
   :rtype: float
   :Game Scenes: Flight





.. attribute:: warp_factor

   The current warp factor. This is the index of the rate at which time
   is passing for either regular "on-rails" or physical time warp. Returns 0
   if time warp is not active. When in on-rails time warp, this is equal to
   :attr:`rails_warp_factor`, and in physics time warp, this is equal to
   :attr:`physics_warp_factor`.

   :Attribute: Read-only, cannot be set
   :rtype: float
   :Game Scenes: Flight





.. attribute:: rails_warp_factor

   The time warp rate, using regular "on-rails" time warp. A value between
   0 and 7 inclusive. 0 means no time warp. Returns 0 if physical time warp
   is active.

   If requested time warp factor cannot be set, it will be set to the next
   lowest possible value. For example, if the vessel is too close to a
   planet. See `the KSP wiki <https://wiki.kerbalspaceprogram.com/wiki/Time_warp>`_ for details.

   :Attribute: Can be read or written
   :rtype: int
   :Game Scenes: Flight





.. attribute:: physics_warp_factor

   The physical time warp rate. A value between 0 and 3 inclusive. 0 means
   no time warp. Returns 0 if regular "on-rails" time warp is active.

   :Attribute: Can be read or written
   :rtype: int
   :Game Scenes: Flight





.. staticmethod:: can_rails_warp_at([factor = 1])

   Returns ``True`` if regular "on-rails" time warp can be used, at the specified warp
   *factor*. The maximum time warp rate is limited by various things,
   including how close the active vessel is to a planet. See
   `the KSP wiki <https://wiki.kerbalspaceprogram.com/wiki/Time_warp>`_
   for details.

   :param int factor: The warp factor to check.
   :rtype: bool
   :Game Scenes: Flight





.. attribute:: maximum_rails_warp_factor

   The current maximum regular "on-rails" warp factor that can be set.
   A value between 0 and 7 inclusive. See
   `the KSP wiki <https://wiki.kerbalspaceprogram.com/wiki/Time_warp>`_
   for details.

   :Attribute: Read-only, cannot be set
   :rtype: int
   :Game Scenes: Flight





.. staticmethod:: warp_to(ut, [max_rails_rate = 100000.0], [max_physics_rate = 2.0])

   Uses time acceleration to warp forward to a time in the future, specified
   by universal time *ut*. This call blocks until the desired
   time is reached. Uses regular "on-rails" or physical time warp as appropriate.
   For example, physical time warp is used when the active vessel is traveling
   through an atmosphere. When using regular "on-rails" time warp, the warp
   rate is limited by *max_rails_rate*, and when using physical
   time warp, the warp rate is limited by *max_physics_rate*.

   :param float ut: The universal time to warp to, in seconds.
   :param float max_rails_rate: The maximum warp rate in regular "on-rails" time warp.
   :param float max_physics_rate: The maximum warp rate in physical time warp.
   :returns: When the time warp is complete.
   :Game Scenes: Flight





.. staticmethod:: transform_position(position, from, to)

   Converts a position from one reference frame to another.

   :param tuple position: Position, as a vector, in reference frame *from*.
   :param ReferenceFrame from: The reference frame that the position is in.
   :param ReferenceFrame to: The reference frame to covert the position to.
   :returns: The corresponding position, as a vector, in reference frame *to*.
   :rtype: tuple(float, float, float)
   




.. staticmethod:: transform_direction(direction, from, to)

   Converts a direction from one reference frame to another.

   :param tuple direction: Direction, as a vector, in reference frame *from*.
   :param ReferenceFrame from: The reference frame that the direction is in.
   :param ReferenceFrame to: The reference frame to covert the direction to.
   :returns: The corresponding direction, as a vector, in reference frame *to*.
   :rtype: tuple(float, float, float)
   




.. staticmethod:: transform_rotation(rotation, from, to)

   Converts a rotation from one reference frame to another.

   :param tuple rotation: Rotation, as a quaternion of the form :math:`(x, y, z, w)`, in reference frame *from*.
   :param ReferenceFrame from: The reference frame that the rotation is in.
   :param ReferenceFrame to: The reference frame to covert the rotation to.
   :returns: The corresponding rotation, as a quaternion of the form :math:`(x, y, z, w)`, in reference frame *to*.
   :rtype: tuple(float, float, float, float)
   




.. staticmethod:: transform_velocity(position, velocity, from, to)

   Converts a velocity (acting at the specified position) from one reference frame
   to another. The position is required to take the relative angular velocity of the
   reference frames into account.

   :param tuple position: Position, as a vector, in reference frame *from*.
   :param tuple velocity: Velocity, as a vector that points in the direction of travel and whose magnitude is the speed in meters per second, in reference frame *from*.
   :param ReferenceFrame from: The reference frame that the position and velocity are in.
   :param ReferenceFrame to: The reference frame to covert the velocity to.
   :returns: The corresponding velocity, as a vector, in reference frame *to*.
   :rtype: tuple(float, float, float)
   




.. staticmethod:: raycast_distance(position, direction, reference_frame)

   Cast a ray from a given position in a given direction, and return the distance to the hit point.
   If no hit occurs, returns infinity.

   :param tuple position: Position, as a vector, of the origin of the ray.
   :param tuple direction: Direction of the ray, as a unit vector.
   :param ReferenceFrame reference_frame: The reference frame that the position and direction are in.
   :returns: The distance to the hit, in meters, or infinity if there was no hit.
   :rtype: float
   




.. staticmethod:: raycast_part(position, direction, reference_frame)

   Cast a ray from a given position in a given direction, and return the part that it hits.
   If no hit occurs, returns ``None``.

   :param tuple position: Position, as a vector, of the origin of the ray.
   :param tuple direction: Direction of the ray, as a unit vector.
   :param ReferenceFrame reference_frame: The reference frame that the position and direction are in.
   :returns: The part that was hit or ``None`` if there was no hit.
   :rtype: :class:`Part`
   :Game Scenes: Flight





.. attribute:: far_available

   Whether `Ferram Aerospace Research <https://forum.kerbalspaceprogram.com/index.php?/topic/19321-130-ferram-aerospace-research-v0159-liebe-82117/>`_ is installed.

   :Attribute: Read-only, cannot be set
   :rtype: bool
   




.. staticmethod:: create_kerbal(name, job, male)

   Creates a Kerbal.

   :param str name:
   :param str job:
   :param bool male:
   




.. staticmethod:: get_kerbal(name)

   Find a Kerbal by name.

   :param str name:
   :rtype: :class:`CrewMember`
   




.. staticmethod:: load_space_center()

   Switch to the space center view.

   




.. attribute:: map_filter

   The visible objects in map mode.

   :Attribute: Can be read or written
   :rtype: :class:`MapFilterType`
   




.. staticmethod:: screenshot(file_path, [scale = 1])

   Saves a screenshot.

   :param str file_path: The path of the file to save.
   :param int scale: Resolution scaling factor
   :Game Scenes: Flight





.. attribute:: game_mode

   The current mode the game is in.

   :Attribute: Read-only, cannot be set
   :rtype: :class:`GameMode`
   




.. attribute:: warp_mode

   The current time warp mode. Returns :attr:`WarpMode.none` if time
   warp is not active, :attr:`WarpMode.rails` if regular "on-rails" time warp
   is active, or :attr:`WarpMode.physics` if physical time warp is active.

   :Attribute: Read-only, cannot be set
   :rtype: :class:`WarpMode`
   :Game Scenes: Flight





.. attribute:: camera

   An object that can be used to control the camera.

   :Attribute: Read-only, cannot be set
   :rtype: :class:`Camera`
   :Game Scenes: Flight





.. attribute:: waypoint_manager

   The waypoint manager.

   :Attribute: Read-only, cannot be set
   :rtype: :class:`WaypointManager`
   :Game Scenes: Flight





.. attribute:: contract_manager

   The contract manager.

   :Attribute: Read-only, cannot be set
   :rtype: :class:`ContractManager`
   




.. attribute:: alarm_manager

   The alarm manager.

   :Attribute: Read-only, cannot be set
   :rtype: :class:`AlarmManager`
   





.. class:: GameMode

   The game mode.
   Returned by :class:`GameMode`


   .. data:: sandbox

      Sandbox mode.


   .. data:: career

      Career mode.


   .. data:: science

      Science career mode.


   .. data:: science_sandbox

      Science sandbox mode.


   .. data:: mission

      Mission mode.


   .. data:: mission_builder

      Mission builder mode.


   .. data:: scenario

      Scenario mode.


   .. data:: scenario_non_resumable

      Scenario mode that cannot be resumed.



.. class:: WarpMode

   The time warp mode.
   Returned by :class:`WarpMode`


   .. data:: rails

      Time warp is active, and in regular "on-rails" mode.


   .. data:: physics

      Time warp is active, and in physical time warp mode.


   .. data:: none

      Time warp is not active.



.. class:: MapFilterType

   The set of things that are visible in map mode.
   These may be combined with bitwise logic.


   .. data:: all

      Everything.


   .. data:: none

      Nothing.


   .. data:: debris

      Debris.


   .. data:: unknown

      Unknown.


   .. data:: space_objects

      SpaceObjects.


   .. data:: probes

      Probes.


   .. data:: rovers

      Rovers.


   .. data:: landers

      Landers.


   .. data:: ships

      Ships.


   .. data:: stations

      Stations.


   .. data:: bases

      Bases.


   .. data:: ev_as

      EVAs.


   .. data:: flags

      Flags.


   .. data:: plane

      Planes.


   .. data:: relay

      Relays.


   .. data:: site

      Launch Sites.


   .. data:: deployed_science_controller

      Deployed Science Controllers.



.. class:: LaunchSite

   A place where craft can be launched from.
   More of these can be added with mods like Kerbal Konstructs.

   .. attribute:: name

      The name of the launch site.

      :Attribute: Read-only, cannot be set
      :rtype: str
   

   .. attribute:: body

      The celestial body the launch site is on.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`CelestialBody`
   

   .. attribute:: editor_facility

      Which editor is normally used for this launch site.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`EditorFacility`
   



.. class:: EditorFacility

   Editor facility.
   See :attr:`LaunchSite.editor_facility`.


   .. data:: vab

      Vehicle Assembly Building.


   .. data:: sph

      Space Plane Hanger.


   .. data:: none

      None.

.. default-domain:: py
.. highlight:: py
.. currentmodule:: SpaceCenter

Vessel
======


.. class:: Vessel

   These objects are used to interact with vessels in KSP. This includes getting
   orbital and flight data, manipulating control inputs and managing resources.
   Created using :attr:`active_vessel` or :attr:`vessels`.

   .. attribute:: name

      The name of the vessel.

      :Attribute: Can be read or written
      :rtype: str
   

   .. attribute:: type

      The type of the vessel.

      :Attribute: Can be read or written
      :rtype: :class:`VesselType`
   

   .. attribute:: situation

      The situation the vessel is in.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`VesselSituation`
   

   .. attribute:: recoverable

      Whether the vessel is recoverable.

      :Attribute: Read-only, cannot be set
      :rtype: bool
   

   .. method:: recover()

      Recover the vessel.

   

   .. attribute:: met

      The mission elapsed time in seconds.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: biome

      The name of the biome the vessel is currently in.

      :Attribute: Read-only, cannot be set
      :rtype: str
   

   .. method:: flight([reference_frame = None])

      Returns a :class:`Flight` object that can be used to get flight
      telemetry for the vessel, in the specified reference frame.

      :param ReferenceFrame reference_frame: Reference frame. Defaults to the vessel's surface reference frame (:attr:`Vessel.surface_reference_frame`).
      :rtype: :class:`Flight`
      :Game Scenes: Flight


      .. note:: When this is called with no arguments, the vessel's surface reference
                frame is used. This reference frame moves with the vessel, therefore
                velocities and speeds returned by the flight object will be zero. See
                the :rst:ref:`reference frames tutorial <tutorial-reference-frames>`
                for examples of getting :rst:ref:`the orbital and surface speeds of a
                vessel <tutorial-reference-frames-vessel-speed>`.

   .. attribute:: orbit

      The current orbit of the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`Orbit`
   

   .. attribute:: control

      Returns a :class:`Control` object that can be used to manipulate
      the vessel's control inputs. For example, its pitch/yaw/roll controls,
      RCS and thrust.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`Control`
      :Game Scenes: Flight

   .. attribute:: comms

      Returns a :class:`Comms` object that can be used to interact
      with CommNet for this vessel.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`Comms`
      :Game Scenes: Flight

   .. attribute:: auto_pilot

      An :class:`AutoPilot` object, that can be used to perform
      simple auto-piloting of the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`AutoPilot`
      :Game Scenes: Flight

   .. attribute:: crew_capacity

      The number of crew that can occupy the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: int
   

   .. attribute:: crew_count

      The number of crew that are occupying the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: int
   

   .. attribute:: crew

      The crew in the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: list(:class:`CrewMember`)
   

   .. attribute:: resources

      A :class:`Resources` object, that can used to get information
      about resources stored in the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`Resources`
      :Game Scenes: Flight

   .. method:: resources_in_decouple_stage(stage, [cumulative = True])

      Returns a :class:`Resources` object, that can used to get
      information about resources stored in a given *stage*.

      :param int stage: Get resources for parts that are decoupled in this stage.
      :param bool cumulative: When ``False``, returns the resources for parts decoupled in just the given stage. When ``True`` returns the resources decoupled in the given stage and all subsequent stages combined.
      :rtype: :class:`Resources`
      :Game Scenes: Flight


      .. note:: For details on stage numbering, see the
                discussion on :rst:ref:`python-api-parts-staging`.

   .. attribute:: parts

      A :class:`Parts` object, that can used to interact with the parts that make up this vessel.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`Parts`
      :Game Scenes: Flight

   .. attribute:: mass

      The total mass of the vessel, including resources, in kg.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: dry_mass

      The total mass of the vessel, excluding resources, in kg.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: thrust

      The total thrust currently being produced by the vessel's engines, in
      Newtons. This is computed by summing :attr:`Engine.thrust` for
      every engine in the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: available_thrust

      Gets the total available thrust that can be produced by the vessel's
      active engines, in Newtons. This is computed by summing
      :attr:`Engine.available_thrust` for every active engine in the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. method:: available_thrust_at(pressure)

      Gets the total available thrust that can be produced by the vessel's
      active engines, in Newtons. This is computed by summing
      :meth:`Engine.available_thrust_at` for every active engine in the vessel.
      Takes the given pressure into account.

      :param float pressure: Atmospheric pressure in atmospheres
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: max_thrust

      The total maximum thrust that can be produced by the vessel's active
      engines, in Newtons. This is computed by summing
      :attr:`Engine.max_thrust` for every active engine.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. method:: max_thrust_at(pressure)

      The total maximum thrust that can be produced by the vessel's active
      engines, in Newtons. This is computed by summing
      :meth:`Engine.max_thrust_at` for every active engine.
      Takes the given pressure into account.

      :param float pressure: Atmospheric pressure in atmospheres
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: max_vacuum_thrust

      The total maximum thrust that can be produced by the vessel's active
      engines when the vessel is in a vacuum, in Newtons. This is computed by
      summing :attr:`Engine.max_vacuum_thrust` for every active engine.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: specific_impulse

      The combined specific impulse of all active engines, in seconds. This is computed using the formula
      `described here <https://wiki.kerbalspaceprogram.com/wiki/Specific_impulse#Multiple_engines>`_.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. method:: specific_impulse_at(pressure)

      The combined specific impulse of all active engines, in seconds. This is computed using the formula
      `described here <https://wiki.kerbalspaceprogram.com/wiki/Specific_impulse#Multiple_engines>`_.
      Takes the given pressure into account.

      :param float pressure: Atmospheric pressure in atmospheres
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: vacuum_specific_impulse

      The combined vacuum specific impulse of all active engines, in seconds. This is computed using the formula
      `described here <https://wiki.kerbalspaceprogram.com/wiki/Specific_impulse#Multiple_engines>`_.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: kerbin_sea_level_specific_impulse

      The combined specific impulse of all active engines at sea level on Kerbin, in seconds.
      This is computed using the formula
      `described here <https://wiki.kerbalspaceprogram.com/wiki/Specific_impulse#Multiple_engines>`_.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: moment_of_inertia

      The moment of inertia of the vessel around its center of mass in :math:`kg.m^2`.
      The inertia values in the returned 3-tuple are around the
      pitch, roll and yaw directions respectively.
      This corresponds to the vessels reference frame (:class:`ReferenceFrame`).

      :Attribute: Read-only, cannot be set
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: inertia_tensor

      The inertia tensor of the vessel around its center of mass,
      in the vessels reference frame (:class:`ReferenceFrame`).
      Returns the 3x3 matrix as a list of elements, in row-major order.

      :Attribute: Read-only, cannot be set
      :rtype: list(float)
   

   .. attribute:: available_torque

      The maximum torque that the vessel generates. Includes contributions from
      reaction wheels, RCS, gimballed engines and aerodynamic control surfaces.
      Returns the torques in :math:`N.m` around each of the coordinate axes of the
      vessels reference frame (:class:`ReferenceFrame`).
      These axes are equivalent to the pitch, roll and yaw axes of the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: tuple(tuple(float, float, float), tuple(float, float, float))
      :Game Scenes: Flight

   .. attribute:: available_reaction_wheel_torque

      The maximum torque that the currently active and powered reaction wheels can generate.
      Returns the torques in :math:`N.m` around each of the coordinate axes of the
      vessels reference frame (:class:`ReferenceFrame`).
      These axes are equivalent to the pitch, roll and yaw axes of the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: tuple(tuple(float, float, float), tuple(float, float, float))
      :Game Scenes: Flight

   .. attribute:: available_rcs_torque

      The maximum torque that the currently active RCS thrusters can generate.
      Returns the torques in :math:`N.m` around each of the coordinate axes of the
      vessels reference frame (:class:`ReferenceFrame`).
      These axes are equivalent to the pitch, roll and yaw axes of the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: tuple(tuple(float, float, float), tuple(float, float, float))
      :Game Scenes: Flight

   .. attribute:: available_rcs_force

      The maximum force that the currently active RCS thrusters can generate.
      Returns the forces in :math:`N` along each of the coordinate axes of the
      vessels reference frame (:class:`ReferenceFrame`).
      These axes are equivalent to the right, forward and bottom directions of the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: tuple(tuple(float, float, float), tuple(float, float, float))
      :Game Scenes: Flight

   .. attribute:: available_engine_torque

      The maximum torque that the currently active and gimballed engines can generate.
      Returns the torques in :math:`N.m` around each of the coordinate axes of the
      vessels reference frame (:class:`ReferenceFrame`).
      These axes are equivalent to the pitch, roll and yaw axes of the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: tuple(tuple(float, float, float), tuple(float, float, float))
      :Game Scenes: Flight

   .. attribute:: available_control_surface_torque

      The maximum torque that the aerodynamic control surfaces can generate.
      Returns the torques in :math:`N.m` around each of the coordinate axes of the
      vessels reference frame (:class:`ReferenceFrame`).
      These axes are equivalent to the pitch, roll and yaw axes of the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: tuple(tuple(float, float, float), tuple(float, float, float))
      :Game Scenes: Flight

   .. attribute:: available_other_torque

      The maximum torque that parts (excluding reaction wheels, gimballed engines,
      RCS and control surfaces) can generate.
      Returns the torques in :math:`N.m` around each of the coordinate axes of the
      vessels reference frame (:class:`ReferenceFrame`).
      These axes are equivalent to the pitch, roll and yaw axes of the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: tuple(tuple(float, float, float), tuple(float, float, float))
      :Game Scenes: Flight

   .. attribute:: reference_frame

      The reference frame that is fixed relative to the vessel,
      and orientated with the vessel.

      * The origin is at the center of mass of the vessel.
      * The axes rotate with the vessel.
      * The x-axis points out to the right of the vessel.
      * The y-axis points in the forward direction of the vessel.
      * The z-axis points out of the bottom off the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`ReferenceFrame`
      :Game Scenes: Flight


      .. figure:: /images/reference-frames/vessel-aircraft.png
         :align: center

         Vessel reference frame origin and axes for the Aeris 3A aircraft

      .. figure:: /images/reference-frames/vessel-rocket.png
         :align: center

         Vessel reference frame origin and axes for the Kerbal-X rocket

   .. attribute:: orbital_reference_frame

      The reference frame that is fixed relative to the vessel,
      and orientated with the vessels orbital prograde/normal/radial directions.

      * The origin is at the center of mass of the vessel.
      * The axes rotate with the orbital prograde/normal/radial directions.
      * The x-axis points in the orbital anti-radial direction.
      * The y-axis points in the orbital prograde direction.
      * The z-axis points in the orbital normal direction.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`ReferenceFrame`
      :Game Scenes: Flight


      .. note::

         Be careful not to confuse this with 'orbit' mode on the navball.

      .. figure:: /images/reference-frames/vessel-orbital.png
         :align: center

         Vessel orbital reference frame origin and axes

   .. attribute:: surface_reference_frame

      The reference frame that is fixed relative to the vessel,
      and orientated with the surface of the body being orbited.

      * The origin is at the center of mass of the vessel.
      * The axes rotate with the north and up directions on the surface of the body.
      * The x-axis points in the `zenith <https://en.wikipedia.org/wiki/Zenith>`_
        direction (upwards, normal to the body being orbited, from the center of the body towards the center of
        mass of the vessel).
      * The y-axis points northwards towards the
        `astronomical horizon <https://en.wikipedia.org/wiki/Horizon>`_ (north, and tangential to the
        surface of the body -- the direction in which a compass would point when on the surface).
      * The z-axis points eastwards towards the
        `astronomical horizon <https://en.wikipedia.org/wiki/Horizon>`_ (east, and tangential to the
        surface of the body -- east on a compass when on the surface).

      :Attribute: Read-only, cannot be set
      :rtype: :class:`ReferenceFrame`
      :Game Scenes: Flight


      .. note::

         Be careful not to confuse this with 'surface' mode on the navball.

      .. figure:: /images/reference-frames/vessel-surface.png
         :align: center

         Vessel surface reference frame origin and axes

   .. attribute:: surface_velocity_reference_frame

      The reference frame that is fixed relative to the vessel,
      and orientated with the velocity vector of the vessel relative
      to the surface of the body being orbited.

      * The origin is at the center of mass of the vessel.
      * The axes rotate with the vessel's velocity vector.
      * The y-axis points in the direction of the vessel's velocity vector,
        relative to the surface of the body being orbited.
      * The z-axis is in the plane of the
        `astronomical horizon <https://en.wikipedia.org/wiki/Horizon>`_.
      * The x-axis is orthogonal to the other two axes.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`ReferenceFrame`
      :Game Scenes: Flight


      .. figure:: /images/reference-frames/vessel-surface-velocity.png
         :align: center

         Vessel surface velocity reference frame origin and axes

   .. method:: position(reference_frame)

      The position of the center of mass of the vessel, in the given reference frame.

      :param ReferenceFrame reference_frame: The reference frame that the returned position vector is in.
      :returns: The position as a vector.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. method:: bounding_box(reference_frame)

      The axis-aligned bounding box of the vessel in the given reference frame.

      :param ReferenceFrame reference_frame: The reference frame that the returned position vectors are in.
      :returns: The positions of the minimum and maximum vertices of the box, as position vectors.
      :rtype: tuple(tuple(float, float, float), tuple(float, float, float))
      :Game Scenes: Flight

   .. method:: velocity(reference_frame)

      The velocity of the center of mass of the vessel, in the given reference frame.

      :param ReferenceFrame reference_frame: The reference frame that the returned velocity vector is in.
      :returns: The velocity as a vector. The vector points in the direction of travel, and its magnitude is the speed of the body in meters per second.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. method:: rotation(reference_frame)

      The rotation of the vessel, in the given reference frame.

      :param ReferenceFrame reference_frame: The reference frame that the returned rotation is in.
      :returns: The rotation as a quaternion of the form :math:`(x, y, z, w)`.
      :rtype: tuple(float, float, float, float)
      :Game Scenes: Flight

   .. method:: direction(reference_frame)

      The direction in which the vessel is pointing, in the given reference frame.

      :param ReferenceFrame reference_frame: The reference frame that the returned direction is in.
      :returns: The direction as a unit vector.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. method:: angular_velocity(reference_frame)

      The angular velocity of the vessel, in the given reference frame.

      :param ReferenceFrame reference_frame: The reference frame the returned angular velocity is in.
      :returns: The angular velocity as a vector. The magnitude of the vector is the rotational speed of the vessel, in radians per second. The direction of the vector indicates the axis of rotation, using the right-hand rule.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight



.. class:: VesselType

   The type of a vessel.
   See :attr:`Vessel.type`.


   .. data:: base

      Base.


   .. data:: debris

      Debris.


   .. data:: lander

      Lander.


   .. data:: plane

      Plane.


   .. data:: probe

      Probe.


   .. data:: relay

      Relay.


   .. data:: rover

      Rover.


   .. data:: ship

      Ship.


   .. data:: station

      Station.


   .. data:: space_object

      SpaceObject.


   .. data:: unknown

      Unknown.


   .. data:: eva

      EVA.


   .. data:: flag

      Flag.


   .. data:: deployed_science_controller

      DeployedScienceController.


   .. data:: deployed_science_part

      DeploedSciencePart.


   .. data:: dropped_part

      DroppedPart.


   .. data:: deployed_ground_part

      DeployedGroundPart.



.. class:: VesselSituation

   The situation a vessel is in.
   See :attr:`Vessel.situation`.


   .. data:: docked

      Vessel is docked to another.


   .. data:: escaping

      Escaping.


   .. data:: flying

      Vessel is flying through an atmosphere.


   .. data:: landed

      Vessel is landed on the surface of a body.


   .. data:: orbiting

      Vessel is orbiting a body.


   .. data:: pre_launch

      Vessel is awaiting launch.


   .. data:: splashed

      Vessel has splashed down in an ocean.


   .. data:: sub_orbital

      Vessel is on a sub-orbital trajectory.



.. class:: CrewMember

   Represents crew in a vessel. Can be obtained using :attr:`Vessel.crew`.

   .. attribute:: name

      The crew members name.

      :Attribute: Can be read or written
      :rtype: str
   

   .. attribute:: type

      The type of crew member.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`CrewMemberType`
   

   .. attribute:: on_mission

      Whether the crew member is on a mission.

      :Attribute: Read-only, cannot be set
      :rtype: bool
   

   .. attribute:: courage

      The crew members courage.

      :Attribute: Can be read or written
      :rtype: float
   

   .. attribute:: stupidity

      The crew members stupidity.

      :Attribute: Can be read or written
      :rtype: float
   

   .. attribute:: experience

      The crew members experience.

      :Attribute: Can be read or written
      :rtype: float
   

   .. attribute:: badass

      Whether the crew member is a badass.

      :Attribute: Can be read or written
      :rtype: bool
   

   .. attribute:: veteran

      Whether the crew member is a veteran.

      :Attribute: Can be read or written
      :rtype: bool
   

   .. attribute:: trait

      The crew member's job.

      :Attribute: Read-only, cannot be set
      :rtype: str
   

   .. attribute:: gender

      The crew member's gender.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`CrewMemberGender`
   

   .. attribute:: roster_status

      The crew member's current roster status.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`RosterStatus`
   

   .. attribute:: suit_type

      The crew member's suit type.

      :Attribute: Can be read or written
      :rtype: :class:`SuitType`
   

   .. attribute:: career_log_flights

      The flight IDs for each entry in the career flight log.

      :Attribute: Read-only, cannot be set
      :rtype: list(int)
   

   .. attribute:: career_log_types

      The type for each entry in the career flight log.

      :Attribute: Read-only, cannot be set
      :rtype: list(str)
   

   .. attribute:: career_log_targets

      The body name for each entry in the career flight log.

      :Attribute: Read-only, cannot be set
      :rtype: list(str)
   



.. class:: CrewMemberType

   The type of a crew member.
   See :attr:`CrewMember.type`.


   .. data:: applicant

      An applicant for crew.


   .. data:: crew

      Rocket crew.


   .. data:: tourist

      A tourist.


   .. data:: unowned

      An unowned crew member.



.. class:: CrewMemberGender

   A crew member's gender.
   See :attr:`CrewMember.gender`.


   .. data:: male

      Male.


   .. data:: female

      Female.



.. class:: RosterStatus

   A crew member's roster status.
   See :attr:`CrewMember.roster_status`.


   .. data:: available

      Available.


   .. data:: assigned

      Assigned.


   .. data:: dead

      Dead.


   .. data:: missing

      Missing.



.. class:: SuitType

   A crew member's suit type.
   See :attr:`CrewMember.suit_type`.


   .. data:: default

      Default.


   .. data:: vintage

      Vintage.


   .. data:: future

      Future.


   .. data:: slim

      Slim.

.. default-domain:: py
.. highlight:: py
.. currentmodule:: SpaceCenter

CelestialBody
=============


.. class:: CelestialBody

   Represents a celestial body (such as a planet or moon).
   See :attr:`bodies`.

   .. attribute:: name

      The name of the body.

      :Attribute: Read-only, cannot be set
      :rtype: str
   

   .. attribute:: satellites

      A list of celestial bodies that are in orbit around this celestial body.

      :Attribute: Read-only, cannot be set
      :rtype: list(:class:`CelestialBody`)
   

   .. attribute:: orbit

      The orbit of the body.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`Orbit`
   

   .. attribute:: mass

      The mass of the body, in kilograms.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: gravitational_parameter

      The `standard gravitational parameter <https://en.wikipedia.org/wiki/Standard_gravitational_parameter>`_ of the body in :math:`m^3s^{-2}`.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: surface_gravity

      The acceleration due to gravity at sea level (mean altitude) on the body,
      in :math:`m/s^2`.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: rotational_period

      The sidereal rotational period of the body, in seconds.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: rotational_speed

      The rotational speed of the body, in radians per second.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: rotation_angle

      The current rotation angle of the body, in radians.
      A value between 0 and :math:`2\pi`

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: initial_rotation

      The initial rotation angle of the body (at UT 0), in radians.
      A value between 0 and :math:`2\pi`

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: equatorial_radius

      The equatorial radius of the body, in meters.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. method:: surface_height(latitude, longitude)

      The height of the surface relative to mean sea level, in meters,
      at the given position. When over water this is equal to 0.

      :param float latitude: Latitude in degrees.
      :param float longitude: Longitude in degrees.
      :rtype: float
   

   .. method:: bedrock_height(latitude, longitude)

      The height of the surface relative to mean sea level, in meters,
      at the given position. When over water, this is the height
      of the sea-bed and is therefore  negative value.

      :param float latitude: Latitude in degrees.
      :param float longitude: Longitude in degrees.
      :rtype: float
   

   .. method:: msl_position(latitude, longitude, reference_frame)

      The position at mean sea level at the given latitude and longitude,
      in the given reference frame.

      :param float latitude: Latitude in degrees.
      :param float longitude: Longitude in degrees.
      :param ReferenceFrame reference_frame: Reference frame for the returned position vector.
      :returns: Position as a vector.
      :rtype: tuple(float, float, float)
   

   .. method:: surface_position(latitude, longitude, reference_frame)

      The position of the surface at the given latitude and longitude, in the given
      reference frame. When over water, this is the position of the surface of the water.

      :param float latitude: Latitude in degrees.
      :param float longitude: Longitude in degrees.
      :param ReferenceFrame reference_frame: Reference frame for the returned position vector.
      :returns: Position as a vector.
      :rtype: tuple(float, float, float)
   

   .. method:: bedrock_position(latitude, longitude, reference_frame)

      The position of the surface at the given latitude and longitude, in the given
      reference frame. When over water, this is the position at the bottom of the sea-bed.

      :param float latitude: Latitude in degrees.
      :param float longitude: Longitude in degrees.
      :param ReferenceFrame reference_frame: Reference frame for the returned position vector.
      :returns: Position as a vector.
      :rtype: tuple(float, float, float)
   

   .. method:: position_at_altitude(latitude, longitude, altitude, reference_frame)

      The position at the given latitude, longitude and altitude, in the given reference frame.

      :param float latitude: Latitude in degrees.
      :param float longitude: Longitude in degrees.
      :param float altitude: Altitude in meters above sea level.
      :param ReferenceFrame reference_frame: Reference frame for the returned position vector.
      :returns: Position as a vector.
      :rtype: tuple(float, float, float)
   

   .. method:: altitude_at_position(position, reference_frame)

      The altitude, in meters, of the given position in the given reference frame.

      :param tuple position: Position as a vector.
      :param ReferenceFrame reference_frame: Reference frame for the position vector.
      :rtype: float
   

   .. method:: latitude_at_position(position, reference_frame)

      The latitude of the given position, in the given reference frame.

      :param tuple position: Position as a vector.
      :param ReferenceFrame reference_frame: Reference frame for the position vector.
      :rtype: float
   

   .. method:: longitude_at_position(position, reference_frame)

      The longitude of the given position, in the given reference frame.

      :param tuple position: Position as a vector.
      :param ReferenceFrame reference_frame: Reference frame for the position vector.
      :rtype: float
   

   .. attribute:: sphere_of_influence

      The radius of the sphere of influence of the body, in meters.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: is_star

      Whether or not the body is a star.

      :Attribute: Read-only, cannot be set
      :rtype: bool
   

   .. attribute:: has_solid_surface

      Whether or not the body has a solid surface.

      :Attribute: Read-only, cannot be set
      :rtype: bool
   

   .. attribute:: has_atmosphere

      ``True`` if the body has an atmosphere.

      :Attribute: Read-only, cannot be set
      :rtype: bool
   

   .. attribute:: atmosphere_depth

      The depth of the atmosphere, in meters.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. method:: atmospheric_density_at_position(position, reference_frame)

      The atmospheric density at the given position, in :math:`kg/m^3`,
      in the given reference frame.

      :param tuple position: The position vector at which to measure the density.
      :param ReferenceFrame reference_frame: Reference frame that the position vector is in.
      :rtype: float
   

   .. attribute:: has_atmospheric_oxygen

      ``True`` if there is oxygen in the atmosphere, required for air-breathing engines.

      :Attribute: Read-only, cannot be set
      :rtype: bool
   

   .. method:: temperature_at(position, reference_frame)

      The temperature on the body at the given position, in the given reference frame.

      :param tuple position: Position as a vector.
      :param ReferenceFrame reference_frame: The reference frame that the position is in.
      :rtype: float
   

      .. note::

         This calculation is performed using the bodies current position, which means that
         the value could be wrong if you want to know the temperature in the far future.

   .. method:: density_at(altitude)

      Gets the air density, in :math:`kg/m^3`, for the specified
      altitude above sea level, in meters.

      :param float altitude:
      :rtype: float
   

      .. note::

         This is an approximation, because actual calculations, taking sun exposure into account
         to compute air temperature, require us to know the exact point on the body where the
         density is to be computed (knowing the altitude is not enough).
         However, the difference is small for high altitudes, so it makes very little difference
         for trajectory prediction.

   .. method:: pressure_at(altitude)

      Gets the air pressure, in Pascals, for the specified
      altitude above sea level, in meters.

      :param float altitude:
      :rtype: float
   

   .. attribute:: biomes

      The biomes present on this body.

      :Attribute: Read-only, cannot be set
      :rtype: set(str)
   

   .. method:: biome_at(latitude, longitude)

      The biome at the given latitude and longitude, in degrees.

      :param float latitude:
      :param float longitude:
      :rtype: str
   

   .. attribute:: flying_high_altitude_threshold

      The altitude, in meters, above which a vessel is considered to be
      flying "high" when doing science.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: space_high_altitude_threshold

      The altitude, in meters, above which a vessel is considered to be
      in "high" space when doing science.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: reference_frame

      The reference frame that is fixed relative to the celestial body.

      * The origin is at the center of the body.
      * The axes rotate with the body.
      * The x-axis points from the center of the body
        towards the intersection of the prime meridian and equator (the
        position at 0° longitude, 0° latitude).
      * The y-axis points from the center of the body
        towards the north pole.
      * The z-axis points from the center of the body
        towards the equator at 90°E longitude.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`ReferenceFrame`
   

      .. figure:: /images/reference-frames/celestial-body.png
         :align: center

         Celestial body reference frame origin and axes. The equator is shown in
         blue, and the prime meridian in red.

   .. attribute:: non_rotating_reference_frame

      The reference frame that is fixed relative to this celestial body, and
      orientated in a fixed direction (it does not rotate with the body).

      * The origin is at the center of the body.
      * The axes do not rotate.
      * The x-axis points in an arbitrary direction through the
        equator.
      * The y-axis points from the center of the body towards
        the north pole.
      * The z-axis points in an arbitrary direction through the
        equator.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`ReferenceFrame`
   

   .. attribute:: orbital_reference_frame

      The reference frame that is fixed relative to this celestial body, but
      orientated with the body's orbital prograde/normal/radial directions.

      * The origin is at the center of the body.
      * The axes rotate with the orbital prograde/normal/radial
        directions.
      * The x-axis points in the orbital anti-radial direction.
      * The y-axis points in the orbital prograde direction.
      * The z-axis points in the orbital normal direction.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`ReferenceFrame`
   

   .. method:: position(reference_frame)

      The position of the center of the body, in the specified reference frame.

      :param ReferenceFrame reference_frame: The reference frame that the returned position vector is in.
      :returns: The position as a vector.
      :rtype: tuple(float, float, float)
   

   .. method:: velocity(reference_frame)

      The linear velocity of the body, in the specified reference frame.

      :param ReferenceFrame reference_frame: The reference frame that the returned velocity vector is in.
      :returns: The velocity as a vector. The vector points in the direction of travel, and its magnitude is the speed of the body in meters per second.
      :rtype: tuple(float, float, float)
   

   .. method:: rotation(reference_frame)

      The rotation of the body, in the specified reference frame.

      :param ReferenceFrame reference_frame: The reference frame that the returned rotation is in.
      :returns: The rotation as a quaternion of the form :math:`(x, y, z, w)`.
      :rtype: tuple(float, float, float, float)
   

   .. method:: direction(reference_frame)

      The direction in which the north pole of the celestial body is pointing,
      in the specified reference frame.

      :param ReferenceFrame reference_frame: The reference frame that the returned direction is in.
      :returns: The direction as a unit vector.
      :rtype: tuple(float, float, float)
   

   .. method:: angular_velocity(reference_frame)

      The angular velocity of the body in the specified reference frame.

      :param ReferenceFrame reference_frame: The reference frame the returned angular velocity is in.
      :returns: The angular velocity as a vector. The magnitude of the vector is the rotational speed of the body, in radians per second. The direction of the vector indicates the axis of rotation, using the right-hand rule.
      :rtype: tuple(float, float, float)

.. default-domain:: py
.. highlight:: py
.. currentmodule:: SpaceCenter

Flight
======


.. class:: Flight

   Used to get flight telemetry for a vessel, by calling :meth:`Vessel.flight`.
   All of the information returned by this class is given in the reference frame
   passed to that method.
   Obtained by calling :meth:`Vessel.flight`.

   .. note::

      To get orbital information, such as the apoapsis or inclination, see :class:`Orbit`.

   .. attribute:: g_force

      The current G force acting on the vessel in :math:`g`.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: mean_altitude

      The altitude above sea level, in meters.
      Measured from the center of mass of the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: surface_altitude

      The altitude above the surface of the body or sea level, whichever is closer, in meters.
      Measured from the center of mass of the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: bedrock_altitude

      The altitude above the surface of the body, in meters. When over water, this is the altitude above the sea floor.
      Measured from the center of mass of the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: elevation

      The elevation of the terrain under the vessel, in meters. This is the height of the terrain above sea level,
      and is negative when the vessel is over the sea.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: latitude

      The `latitude <https://en.wikipedia.org/wiki/Latitude>`_ of the vessel for the body being orbited, in degrees.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: longitude

      The `longitude <https://en.wikipedia.org/wiki/Longitude>`_ of the vessel for the body being orbited, in degrees.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: velocity

      The velocity of the vessel, in the reference frame :class:`ReferenceFrame`.

      :Attribute: Read-only, cannot be set
      :returns: The velocity as a vector. The vector points in the direction of travel, and its magnitude is the speed of the vessel in meters per second.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: speed

      The speed of the vessel in meters per second,
      in the reference frame :class:`ReferenceFrame`.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: horizontal_speed

      The horizontal speed of the vessel in meters per second,
      in the reference frame :class:`ReferenceFrame`.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: vertical_speed

      The vertical speed of the vessel in meters per second,
      in the reference frame :class:`ReferenceFrame`.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: center_of_mass

      The position of the center of mass of the vessel,
      in the reference frame :class:`ReferenceFrame`

      :Attribute: Read-only, cannot be set
      :returns: The position as a vector.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: rotation

      The rotation of the vessel, in the reference frame :class:`ReferenceFrame`

      :Attribute: Read-only, cannot be set
      :returns: The rotation as a quaternion of the form :math:`(x, y, z, w)`.
      :rtype: tuple(float, float, float, float)
      :Game Scenes: Flight

   .. attribute:: direction

      The direction that the vessel is pointing in,
      in the reference frame :class:`ReferenceFrame`.

      :Attribute: Read-only, cannot be set
      :returns: The direction as a unit vector.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: pitch

      The pitch of the vessel relative to the horizon, in degrees.
      A value between -90° and +90°.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: heading

      The heading of the vessel (its angle relative to north), in degrees.
      A value between 0° and 360°.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: roll

      The roll of the vessel relative to the horizon, in degrees.
      A value between -180° and +180°.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: prograde

      The prograde direction of the vessels orbit,
      in the reference frame :class:`ReferenceFrame`.

      :Attribute: Read-only, cannot be set
      :returns: The direction as a unit vector.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: retrograde

      The retrograde direction of the vessels orbit,
      in the reference frame :class:`ReferenceFrame`.

      :Attribute: Read-only, cannot be set
      :returns: The direction as a unit vector.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: normal

      The direction normal to the vessels orbit,
      in the reference frame :class:`ReferenceFrame`.

      :Attribute: Read-only, cannot be set
      :returns: The direction as a unit vector.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: anti_normal

      The direction opposite to the normal of the vessels orbit,
      in the reference frame :class:`ReferenceFrame`.

      :Attribute: Read-only, cannot be set
      :returns: The direction as a unit vector.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: radial

      The radial direction of the vessels orbit,
      in the reference frame :class:`ReferenceFrame`.

      :Attribute: Read-only, cannot be set
      :returns: The direction as a unit vector.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: anti_radial

      The direction opposite to the radial direction of the vessels orbit,
      in the reference frame :class:`ReferenceFrame`.

      :Attribute: Read-only, cannot be set
      :returns: The direction as a unit vector.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: atmosphere_density

      The current density of the atmosphere around the vessel, in :math:`kg/m^3`.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: dynamic_pressure

      The dynamic pressure acting on the vessel, in Pascals. This is a measure of the
      strength of the aerodynamic forces. It is equal to
      :math:`\frac{1}{2} . \mbox{air density} . \mbox{velocity}^2`.
      It is commonly denoted :math:`Q`.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: static_pressure

      The static atmospheric pressure acting on the vessel, in Pascals.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: static_pressure_at_msl

      The static atmospheric pressure at mean sea level, in Pascals.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: aerodynamic_force

      The total aerodynamic forces acting on the vessel,
      in reference frame :class:`ReferenceFrame`.

      :Attribute: Read-only, cannot be set
      :returns: A vector pointing in the direction that the force acts, with its magnitude equal to the strength of the force in Newtons.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. method:: simulate_aerodynamic_force_at(body, position, velocity)

      Simulate and return the total aerodynamic forces acting on the vessel,
      if it where to be traveling with the given velocity at the given position in the
      atmosphere of the given celestial body.

      :param CelestialBody body:
      :param tuple position:
      :param tuple velocity:
      :returns: A vector pointing in the direction that the force acts, with its magnitude equal to the strength of the force in Newtons.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: lift

      The `aerodynamic lift <https://en.wikipedia.org/wiki/Aerodynamic_force>`_
      currently acting on the vessel.

      :Attribute: Read-only, cannot be set
      :returns: A vector pointing in the direction that the force acts, with its magnitude equal to the strength of the force in Newtons.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: drag

      The `aerodynamic drag <https://en.wikipedia.org/wiki/Aerodynamic_force>`_ currently acting on the vessel.

      :Attribute: Read-only, cannot be set
      :returns: A vector pointing in the direction of the force, with its magnitude equal to the strength of the force in Newtons.
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: speed_of_sound

      The speed of sound, in the atmosphere around the vessel, in :math:`m/s`.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: mach

      The speed of the vessel, in multiples of the speed of sound.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: reynolds_number

      The vessels Reynolds number.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight


      .. note::

         Requires `Ferram Aerospace Research <https://forum.kerbalspaceprogram.com/index.php?/topic/19321-130-ferram-aerospace-research-v0159-liebe-82117/>`_.

   .. attribute:: true_air_speed

      The `true air speed <https://en.wikipedia.org/wiki/True_airspeed>`_
      of the vessel, in meters per second.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: equivalent_air_speed

      The `equivalent air speed <https://en.wikipedia.org/wiki/Equivalent_airspeed>`_
      of the vessel, in meters per second.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: terminal_velocity

      An estimate of the current terminal velocity of the vessel, in meters per second.
      This is the speed at which the drag forces cancel out the force of gravity.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: angle_of_attack

      The pitch angle between the orientation of the vessel and its velocity vector,
      in degrees.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: sideslip_angle

      The yaw angle between the orientation of the vessel and its velocity vector, in degrees.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: total_air_temperature

      The `total air temperature <https://en.wikipedia.org/wiki/Total_air_temperature>`_
      of the atmosphere around the vessel, in Kelvin.
      This includes the :attr:`Flight.static_air_temperature` and the vessel's kinetic energy.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: static_air_temperature

      The `static (ambient) temperature <https://en.wikipedia.org/wiki/Total_air_temperature>`_ of the atmosphere around the vessel, in Kelvin.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: stall_fraction

      The current amount of stall, between 0 and 1. A value greater than 0.005 indicates
      a minor stall and a value greater than 0.5 indicates a large-scale stall.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight


      .. note::

         Requires `Ferram Aerospace Research <https://forum.kerbalspaceprogram.com/index.php?/topic/19321-130-ferram-aerospace-research-v0159-liebe-82117/>`_.

   .. attribute:: drag_coefficient

      The coefficient of drag. This is the amount of drag produced by the vessel.
      It depends on air speed, air density and wing area.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight


      .. note::

         Requires `Ferram Aerospace Research <https://forum.kerbalspaceprogram.com/index.php?/topic/19321-130-ferram-aerospace-research-v0159-liebe-82117/>`_.

   .. attribute:: lift_coefficient

      The coefficient of lift. This is the amount of lift produced by the vessel, and
      depends on air speed, air density and wing area.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight


      .. note::

         Requires `Ferram Aerospace Research <https://forum.kerbalspaceprogram.com/index.php?/topic/19321-130-ferram-aerospace-research-v0159-liebe-82117/>`_.

   .. attribute:: ballistic_coefficient

      The `ballistic coefficient <https://en.wikipedia.org/wiki/Ballistic_coefficient>`_.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight


      .. note::

         Requires `Ferram Aerospace Research <https://forum.kerbalspaceprogram.com/index.php?/topic/19321-130-ferram-aerospace-research-v0159-liebe-82117/>`_.

   .. attribute:: thrust_specific_fuel_consumption

      The thrust specific fuel consumption for the jet engines on the vessel. This is a
      measure of the efficiency of the engines, with a lower value indicating a more
      efficient vessel. This value is the number of Newtons of fuel that are burned,
      per hour, to produce one newton of thrust.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight


      .. note::

         Requires `Ferram Aerospace Research <https://forum.kerbalspaceprogram.com/index.php?/topic/19321-130-ferram-aerospace-research-v0159-liebe-82117/>`_.

.. default-domain:: py
.. highlight:: py
.. currentmodule:: SpaceCenter

Orbit
=====


.. class:: Orbit

   Describes an orbit. For example, the orbit of a vessel, obtained by calling
   :attr:`Vessel.orbit`, or a celestial body, obtained by calling
   :attr:`CelestialBody.orbit`.

   .. attribute:: body

      The celestial body (e.g. planet or moon) around which the object is orbiting.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`CelestialBody`
   

   .. attribute:: apoapsis

      Gets the apoapsis of the orbit, in meters, from the center of mass
      of the body being orbited.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

      .. note::

         For the apoapsis altitude reported on the in-game map view,
         use :attr:`Orbit.apoapsis_altitude`.

   .. attribute:: periapsis

      The periapsis of the orbit, in meters, from the center of mass
      of the body being orbited.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

      .. note::

         For the periapsis altitude reported on the in-game map view,
         use :attr:`Orbit.periapsis_altitude`.

   .. attribute:: apoapsis_altitude

      The apoapsis of the orbit, in meters, above the sea level of the body being orbited.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

      .. note::

         This is equal to :attr:`Orbit.apoapsis` minus the equatorial radius of the body.

   .. attribute:: periapsis_altitude

      The periapsis of the orbit, in meters, above the sea level of the body being orbited.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

      .. note::

         This is equal to :attr:`Orbit.periapsis` minus the equatorial radius of the body.

   .. attribute:: semi_major_axis

      The semi-major axis of the orbit, in meters.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: semi_minor_axis

      The semi-minor axis of the orbit, in meters.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: radius

      The current radius of the orbit, in meters. This is the distance between the center
      of mass of the object in orbit, and the center of mass of the body around which it
      is orbiting.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

      .. note::

         This value will change over time if the orbit is elliptical.

   .. method:: radius_at(ut)

      The orbital radius at the given time, in meters.

      :param float ut: The universal time to measure the radius at.
      :rtype: float
   

   .. method:: position_at(ut, reference_frame)

      The position at a given time, in the specified reference frame.

      :param float ut: The universal time to measure the position at.
      :param ReferenceFrame reference_frame: The reference frame that the returned position vector is in.
      :returns: The position as a vector.
      :rtype: tuple(float, float, float)
   

   .. attribute:: speed

      The current orbital speed of the object in meters per second.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

      .. note::

         This value will change over time if the orbit is elliptical.

   .. attribute:: period

      The orbital period, in seconds.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: time_to_apoapsis

      The time until the object reaches apoapsis, in seconds.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: time_to_periapsis

      The time until the object reaches periapsis, in seconds.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: eccentricity

      The `eccentricity <https://en.wikipedia.org/wiki/Orbital_eccentricity>`_
      of the orbit.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: inclination

      The `inclination <https://en.wikipedia.org/wiki/Orbital_inclination>`_
      of the orbit,
      in radians.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: longitude_of_ascending_node

      The `longitude of the ascending node <https://en.wikipedia.org/wiki/Longitude_of_the_ascending_node>`_, in radians.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: argument_of_periapsis

      The `argument of periapsis <https://en.wikipedia.org/wiki/Argument_of_periapsis>`_, in radians.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: mean_anomaly_at_epoch

      The `mean anomaly at epoch <https://en.wikipedia.org/wiki/Mean_anomaly>`_.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: epoch

      The time since the epoch (the point at which the
      `mean anomaly at epoch <https://en.wikipedia.org/wiki/Mean_anomaly>`_
      was measured, in seconds.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: mean_anomaly

      The `mean anomaly <https://en.wikipedia.org/wiki/Mean_anomaly>`_.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. method:: mean_anomaly_at_ut(ut)

      The mean anomaly at the given time.

      :param float ut: The universal time in seconds.
      :rtype: float
   

   .. attribute:: eccentric_anomaly

      The `eccentric anomaly <https://en.wikipedia.org/wiki/Eccentric_anomaly>`_.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. method:: eccentric_anomaly_at_ut(ut)

      The eccentric anomaly at the given universal time.

      :param float ut: The universal time, in seconds.
      :rtype: float
   

   .. attribute:: true_anomaly

      The `true anomaly <https://en.wikipedia.org/wiki/True_anomaly>`_.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. method:: true_anomaly_at_ut(ut)

      The true anomaly at the given time.

      :param float ut: The universal time in seconds.
      :rtype: float
   

   .. method:: true_anomaly_at_radius(radius)

      The true anomaly at the given orbital radius.

      :param float radius: The orbital radius in meters.
      :rtype: float
   

   .. method:: ut_at_true_anomaly(true_anomaly)

      The universal time, in seconds, corresponding to the given true anomaly.

      :param float true_anomaly: True anomaly.
      :rtype: float
   

   .. method:: radius_at_true_anomaly(true_anomaly)

      The orbital radius at the point in the orbit given by the true anomaly.

      :param float true_anomaly: The true anomaly.
      :rtype: float
   

   .. method:: true_anomaly_at_an(target)

      The true anomaly of the ascending node with the given target orbit.

      :param Orbit target: Target orbit.
      :rtype: float
   

   .. method:: true_anomaly_at_dn(target)

      The true anomaly of the descending node with the given target orbit.

      :param Orbit target: Target orbit.
      :rtype: float
   

   .. attribute:: orbital_speed

      The current orbital speed in meters per second.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. method:: orbital_speed_at(time)

      The orbital speed at the given time, in meters per second.

      :param float time: Time from now, in seconds.
      :rtype: float
   

   .. staticmethod:: reference_plane_normal(reference_frame)

      The direction that is normal to the orbits reference plane,
      in the given reference frame.
      The reference plane is the plane from which the orbits inclination is measured.

      :param ReferenceFrame reference_frame: The reference frame that the returned direction is in.
      :returns: The direction as a unit vector.
      :rtype: tuple(float, float, float)
   

   .. staticmethod:: reference_plane_direction(reference_frame)

      The direction from which the orbits longitude of ascending node is measured,
      in the given reference frame.

      :param ReferenceFrame reference_frame: The reference frame that the returned direction is in.
      :returns: The direction as a unit vector.
      :rtype: tuple(float, float, float)
   

   .. method:: relative_inclination(target)

      Relative inclination of this orbit and the target orbit, in radians.

      :param Orbit target: Target orbit.
      :rtype: float
   

   .. attribute:: time_to_soi_change

      The time until the object changes sphere of influence, in seconds. Returns ``NaN``
      if the object is not going to change sphere of influence.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: next_orbit

      If the object is going to change sphere of influence in the future, returns the new
      orbit after the change. Otherwise returns ``None``.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`Orbit`
   

   .. method:: time_of_closest_approach(target)

      Estimates and returns the time at closest approach to a target orbit.

      :param Orbit target: Target orbit.
      :returns: The universal time at closest approach, in seconds.
      :rtype: float
   

   .. method:: distance_at_closest_approach(target)

      Estimates and returns the distance at closest approach to a target orbit, in meters.

      :param Orbit target: Target orbit.
      :rtype: float
   

   .. method:: list_closest_approaches(target, orbits)

      Returns the times at closest approach and corresponding distances, to a target orbit.

      :param Orbit target: Target orbit.
      :param int orbits: The number of future orbits to search.
      :returns: A list of two lists. The first is a list of times at closest approach, as universal times in seconds. The second is a list of corresponding distances at closest approach, in meters.
      :rtype: list(list(float))

.. default-domain:: py
.. highlight:: py
.. currentmodule:: SpaceCenter

Control
=======


.. class:: Control

   Used to manipulate the controls of a vessel. This includes adjusting the
   throttle, enabling/disabling systems such as SAS and RCS, or altering the
   direction in which the vessel is pointing.
   Obtained by calling :attr:`Vessel.control`.

   .. note::

      Control inputs (such as pitch, yaw and roll) are zeroed when all clients
      that have set one or more of these inputs are no longer connected.

   .. attribute:: source

      The source of the vessels control, for example by a kerbal or a probe core.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`ControlSource`
      :Game Scenes: Flight

   .. attribute:: state

      The control state of the vessel.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`ControlState`
      :Game Scenes: Flight

   .. attribute:: sas

      The state of SAS.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight


      .. note::

         Equivalent to :attr:`AutoPilot.sas`

   .. attribute:: sas_mode

      The current :class:`SASMode`.
      These modes are equivalent to the mode buttons to
      the left of the navball that appear when SAS is enabled.

      :Attribute: Can be read or written
      :rtype: :class:`SASMode`
      :Game Scenes: Flight


      .. note::

         Equivalent to :attr:`AutoPilot.sas_mode`

   .. attribute:: speed_mode

      The current :class:`SpeedMode` of the navball.
      This is the mode displayed next to the speed at the top of the navball.

      :Attribute: Can be read or written
      :rtype: :class:`SpeedMode`
      :Game Scenes: Flight

   .. attribute:: rcs

      The state of RCS.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: reaction_wheels

      Returns whether all reactive wheels on the vessel are active,
      and sets the active state of all reaction wheels.
      See :attr:`ReactionWheel.active`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: gear

      The state of the landing gear/legs.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: legs

      Returns whether all landing legs on the vessel are deployed,
      and sets the deployment state of all landing legs.
      Does not include wheels (for example landing gear).
      See :attr:`Leg.deployed`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: wheels

      Returns whether all wheels on the vessel are deployed,
      and sets the deployment state of all wheels.
      Does not include landing legs.
      See :attr:`Wheel.deployed`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: lights

      The state of the lights.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: brakes

      The state of the wheel brakes.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: antennas

      Returns whether all antennas on the vessel are deployed,
      and sets the deployment state of all antennas.
      See :attr:`Antenna.deployed`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: cargo_bays

      Returns whether any of the cargo bays on the vessel are open,
      and sets the open state of all cargo bays.
      See :attr:`CargoBay.open`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: intakes

      Returns whether all of the air intakes on the vessel are open,
      and sets the open state of all air intakes.
      See :attr:`Intake.open`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: parachutes

      Returns whether all parachutes on the vessel are deployed,
      and sets the deployment state of all parachutes.
      Cannot be set to ``False``.
      See :attr:`Parachute.deployed`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: radiators

      Returns whether all radiators on the vessel are deployed,
      and sets the deployment state of all radiators.
      See :attr:`Radiator.deployed`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: resource_harvesters

      Returns whether all of the resource harvesters on the vessel are deployed,
      and sets the deployment state of all resource harvesters.
      See :attr:`ResourceHarvester.deployed`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: resource_harvesters_active

      Returns whether any of the resource harvesters on the vessel are active,
      and sets the active state of all resource harvesters.
      See :attr:`ResourceHarvester.active`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: solar_panels

      Returns whether all solar panels on the vessel are deployed,
      and sets the deployment state of all solar panels.
      See :attr:`SolarPanel.deployed`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: abort

      The state of the abort action group.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: throttle

      The state of the throttle. A value between 0 and 1.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: input_mode

      Sets the behavior of the pitch, yaw, roll and translation control inputs.
      When set to additive, these inputs are added to the vessels current inputs.
      This mode is the default.
      When set to override, these inputs (if non-zero) override the vessels inputs.
      This mode prevents keyboard control, or SAS, from interfering with the controls when
      they are set.

      :Attribute: Can be read or written
      :rtype: :class:`ControlInputMode`
      :Game Scenes: Flight

   .. attribute:: pitch

      The state of the pitch control.
      A value between -1 and 1.
      Equivalent to the w and s keys.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: yaw

      The state of the yaw control.
      A value between -1 and 1.
      Equivalent to the a and d keys.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: roll

      The state of the roll control.
      A value between -1 and 1.
      Equivalent to the q and e keys.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: forward

      The state of the forward translational control.
      A value between -1 and 1.
      Equivalent to the h and n keys.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: up

      The state of the up translational control.
      A value between -1 and 1.
      Equivalent to the i and k keys.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: right

      The state of the right translational control.
      A value between -1 and 1.
      Equivalent to the j and l keys.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: wheel_throttle

      The state of the wheel throttle.
      A value between -1 and 1.
      A value of 1 rotates the wheels forwards, a value of -1 rotates
      the wheels backwards.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: wheel_steering

      The state of the wheel steering.
      A value between -1 and 1.
      A value of 1 steers to the left, and a value of -1 steers to the right.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: custom_axis01

      The state of CustomAxis01.
      A value between -1 and 1.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: custom_axis02

      The state of CustomAxis02.
      A value between -1 and 1.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: custom_axis03

      The state of CustomAxis03.
      A value between -1 and 1.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: custom_axis04

      The state of CustomAxis04.
      A value between -1 and 1.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: current_stage

      The current stage of the vessel. Corresponds to the stage number in
      the in-game UI.

      :Attribute: Read-only, cannot be set
      :rtype: int
      :Game Scenes: Flight

   .. method:: activate_next_stage()

      Activates the next stage. Equivalent to pressing the space bar in-game.

      :returns: A list of vessel objects that are jettisoned from the active vessel.
      :rtype: list(:class:`Vessel`)
      :Game Scenes: Flight


      .. note::

         When called, the active vessel may change. It is therefore possible that,
         after calling this function, the object(s) returned by previous call(s) to
         :attr:`active_vessel` no longer refer to the active vessel.
         Throws an exception if staging is locked.

   .. attribute:: stage_lock

      Whether staging is locked on the vessel.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight


      .. note::

         This is equivalent to locking the staging using Alt+L

   .. method:: get_action_group(group)

      Returns ``True`` if the given action group is enabled.

      :param int group: A number between 0 and 9 inclusive, or between 0 and 250 inclusive when the `Extended Action Groups mod <https://forum.kerbalspaceprogram.com/index.php?/topic/67235-122dec1016-action-groups-extended-250-action-groups-in-flight-editing-now-kosremotetech/>`_ is installed.
      :rtype: bool
      :Game Scenes: Flight

   .. method:: set_action_group(group, state)

      Sets the state of the given action group.

      :param int group: A number between 0 and 9 inclusive, or between 0 and 250 inclusive when the `Extended Action Groups mod <https://forum.kerbalspaceprogram.com/index.php?/topic/67235-122dec1016-action-groups-extended-250-action-groups-in-flight-editing-now-kosremotetech/>`_ is installed.
      :param bool state:
      :Game Scenes: Flight

   .. method:: toggle_action_group(group)

      Toggles the state of the given action group.

      :param int group: A number between 0 and 9 inclusive, or between 0 and 250 inclusive when the `Extended Action Groups mod <https://forum.kerbalspaceprogram.com/index.php?/topic/67235-122dec1016-action-groups-extended-250-action-groups-in-flight-editing-now-kosremotetech/>`_ is installed.
      :Game Scenes: Flight

   .. method:: add_node(ut, [prograde = 0.0], [normal = 0.0], [radial = 0.0])

      Creates a maneuver node at the given universal time, and returns a
      :class:`Node` object that can be used to modify it.
      Optionally sets the magnitude of the delta-v for the maneuver node
      in the prograde, normal and radial directions.

      :param float ut: Universal time of the maneuver node.
      :param float prograde: Delta-v in the prograde direction.
      :param float normal: Delta-v in the normal direction.
      :param float radial: Delta-v in the radial direction.
      :rtype: :class:`Node`
      :Game Scenes: Flight

   .. attribute:: nodes

      Returns a list of all existing maneuver nodes, ordered by time from first to last.

      :Attribute: Read-only, cannot be set
      :rtype: list(:class:`Node`)
      :Game Scenes: Flight

   .. method:: remove_nodes()

      Remove all maneuver nodes.

      :Game Scenes: Flight



.. class:: ControlState

   The control state of a vessel.
   See :attr:`Control.state`.


   .. data:: full

      Full controllable.


   .. data:: partial

      Partially controllable.


   .. data:: none

      Not controllable.



.. class:: ControlSource

   The control source of a vessel.
   See :attr:`Control.source`.


   .. data:: kerbal

      Vessel is controlled by a Kerbal.


   .. data:: probe

      Vessel is controlled by a probe core.


   .. data:: none

      Vessel is not controlled.



.. class:: SASMode

   The behavior of the SAS auto-pilot. See :attr:`AutoPilot.sas_mode`.


   .. data:: stability_assist

      Stability assist mode. Dampen out any rotation.


   .. data:: maneuver

      Point in the burn direction of the next maneuver node.


   .. data:: prograde

      Point in the prograde direction.


   .. data:: retrograde

      Point in the retrograde direction.


   .. data:: normal

      Point in the orbit normal direction.


   .. data:: anti_normal

      Point in the orbit anti-normal direction.


   .. data:: radial

      Point in the orbit radial direction.


   .. data:: anti_radial

      Point in the orbit anti-radial direction.


   .. data:: target

      Point in the direction of the current target.


   .. data:: anti_target

      Point away from the current target.



.. class:: SpeedMode

   The mode of the speed reported in the navball.
   See :attr:`Control.speed_mode`.


   .. data:: orbit

      Speed is relative to the vessel's orbit.


   .. data:: surface

      Speed is relative to the surface of the body being orbited.


   .. data:: target

      Speed is relative to the current target.



.. class:: ControlInputMode

   See :attr:`Control.input_mode`.


   .. data:: additive

      Control inputs are added to the vessels current control inputs.


   .. data:: override

      Control inputs (when they are non-zero) override the vessels current control inputs.

.. default-domain:: py
.. highlight:: py
.. currentmodule:: SpaceCenter

Resources
=========


.. class:: Resources

   Represents the collection of resources stored in a vessel, stage or part.
   Created by calling :attr:`Vessel.resources`,
   :meth:`Vessel.resources_in_decouple_stage` or
   :attr:`Part.resources`.

   .. attribute:: all

      All the individual resources that can be stored.

      :Attribute: Read-only, cannot be set
      :rtype: list(:class:`Resource`)
      :Game Scenes: Flight

   .. method:: with_resource(name)

      All the individual resources with the given name that can be stored.

      :param str name:
      :rtype: list(:class:`Resource`)
      :Game Scenes: Flight

   .. attribute:: names

      A list of resource names that can be stored.

      :Attribute: Read-only, cannot be set
      :rtype: list(str)
      :Game Scenes: Flight

   .. method:: has_resource(name)

      Check whether the named resource can be stored.

      :param str name: The name of the resource.
      :rtype: bool
      :Game Scenes: Flight

   .. method:: amount(name)

      Returns the amount of a resource that is currently stored.

      :param str name: The name of the resource.
      :rtype: float
      :Game Scenes: Flight

   .. method:: max(name)

      Returns the amount of a resource that can be stored.

      :param str name: The name of the resource.
      :rtype: float
      :Game Scenes: Flight

   .. staticmethod:: density(name)

      Returns the density of a resource, in :math:`kg/l`.

      :param str name: The name of the resource.
      :rtype: float
      :Game Scenes: Flight

   .. staticmethod:: flow_mode(name)

      Returns the flow mode of a resource.

      :param str name: The name of the resource.
      :rtype: :class:`ResourceFlowMode`
      :Game Scenes: Flight

   .. attribute:: enabled

      Whether use of all the resources are enabled.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight


      .. note::

         This is ``True`` if all of the resources are enabled.
         If any of the resources are not enabled, this is ``False``.



.. class:: Resource

   An individual resource stored within a part.
   Created using methods in the :class:`Resources` class.

   .. attribute:: name

      The name of the resource.

      :Attribute: Read-only, cannot be set
      :rtype: str
   

   .. attribute:: part

      The part containing the resource.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`Part`
   

   .. attribute:: amount

      The amount of the resource that is currently stored in the part.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: max

      The total amount of the resource that can be stored in the part.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: density

      The density of the resource, in :math:`kg/l`.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: flow_mode

      The flow mode of the resource.

      :Attribute: Read-only, cannot be set
      :rtype: :class:`ResourceFlowMode`
   

   .. attribute:: enabled

      Whether use of this resource is enabled.

      :Attribute: Can be read or written
      :rtype: bool
   



.. class:: ResourceTransfer

   Transfer resources between parts.

   .. staticmethod:: start(from_part, to_part, resource, max_amount)

      Start transferring a resource transfer between a pair of parts. The transfer will move
      at most *max_amount* units of the resource, depending on how much of
      the resource is available in the source part and how much storage is available in the
      destination part.
      Use :attr:`ResourceTransfer.complete` to check if the transfer is complete.
      Use :attr:`ResourceTransfer.amount` to see how much of the resource has been transferred.

      :param Part from_part: The part to transfer to.
      :param Part to_part: The part to transfer from.
      :param str resource: The name of the resource to transfer.
      :param float max_amount: The maximum amount of resource to transfer.
      :rtype: :class:`ResourceTransfer`
   

   .. attribute:: amount

      The amount of the resource that has been transferred.

      :Attribute: Read-only, cannot be set
      :rtype: float
   

   .. attribute:: complete

      Whether the transfer has completed.

      :Attribute: Read-only, cannot be set
      :rtype: bool
   



.. class:: ResourceFlowMode

   The way in which a resource flows between parts. See :meth:`Resources.flow_mode`.


   .. data:: vessel

      The resource flows to any part in the vessel. For example, electric charge.


   .. data:: stage

      The resource flows from parts in the first stage, followed by the second,
      and so on. For example, mono-propellant.


   .. data:: adjacent

      The resource flows between adjacent parts within the vessel. For example,
      liquid fuel or oxidizer.


   .. data:: none

      The resource does not flow. For example, solid fuel.

.. default-domain:: py
.. highlight:: py
.. currentmodule:: SpaceCenter

AutoPilot
=========


.. class:: AutoPilot

   Provides basic auto-piloting utilities for a vessel.
   Created by calling :attr:`Vessel.auto_pilot`.

   .. note::

      If a client engages the auto-pilot and then closes its connection to the server,
      the auto-pilot will be disengaged and its target reference frame, direction and roll
      reset to default.

   .. method:: engage()

      Engage the auto-pilot.

      :Game Scenes: Flight

   .. method:: disengage()

      Disengage the auto-pilot.

      :Game Scenes: Flight

   .. method:: wait()

      Blocks until the vessel is pointing in the target direction and has
      the target roll (if set). Throws an exception if the auto-pilot has not been engaged.

      :Game Scenes: Flight

   .. attribute:: error

      The error, in degrees, between the direction the ship has been asked
      to point in and the direction it is pointing in. Throws an exception if the auto-pilot
      has not been engaged and SAS is not enabled or is in stability assist mode.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: pitch_error

      The error, in degrees, between the vessels current and target pitch.
      Throws an exception if the auto-pilot has not been engaged.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: heading_error

      The error, in degrees, between the vessels current and target heading.
      Throws an exception if the auto-pilot has not been engaged.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: roll_error

      The error, in degrees, between the vessels current and target roll.
      Throws an exception if the auto-pilot has not been engaged or no target roll is set.

      :Attribute: Read-only, cannot be set
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: reference_frame

      The reference frame for the target direction (:attr:`AutoPilot.target_direction`).

      :Attribute: Can be read or written
      :rtype: :class:`ReferenceFrame`
      :Game Scenes: Flight


      .. note::

         An error will be thrown if this property is set to a reference frame that rotates with
         the vessel being controlled, as it is impossible to rotate the vessel in such a
         reference frame.

   .. attribute:: target_pitch

      The target pitch, in degrees, between -90° and +90°.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: target_heading

      The target heading, in degrees, between 0° and 360°.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: target_roll

      The target roll, in degrees. ``NaN`` if no target roll is set.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: target_direction

      Direction vector corresponding to the target pitch and heading.
      This is in the reference frame specified by :class:`ReferenceFrame`.

      :Attribute: Can be read or written
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. method:: target_pitch_and_heading(pitch, heading)

      Set target pitch and heading angles.

      :param float pitch: Target pitch angle, in degrees between -90° and +90°.
      :param float heading: Target heading angle, in degrees between 0° and 360°.
      :Game Scenes: Flight

   .. attribute:: sas

      The state of SAS.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight


      .. note::

         Equivalent to :attr:`Control.sas`

   .. attribute:: sas_mode

      The current :class:`SASMode`.
      These modes are equivalent to the mode buttons to the left of the navball that appear
      when SAS is enabled.

      :Attribute: Can be read or written
      :rtype: :class:`SASMode`
      :Game Scenes: Flight


      .. note::

         Equivalent to :attr:`Control.sas_mode`

   .. attribute:: roll_threshold

      The threshold at which the autopilot will try to match the target roll angle, if any.
      Defaults to 5 degrees.

      :Attribute: Can be read or written
      :rtype: float
      :Game Scenes: Flight

   .. attribute:: stopping_time

      The maximum amount of time that the vessel should need to come to a complete stop.
      This determines the maximum angular velocity of the vessel.
      A vector of three stopping times, in seconds, one for each of the pitch, roll
      and yaw axes. Defaults to 0.5 seconds for each axis.

      :Attribute: Can be read or written
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: deceleration_time

      The time the vessel should take to come to a stop pointing in the target direction.
      This determines the angular acceleration used to decelerate the vessel.
      A vector of three times, in seconds, one for each of the pitch, roll and yaw axes.
      Defaults to 5 seconds for each axis.

      :Attribute: Can be read or written
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: attenuation_angle

      The angle at which the autopilot considers the vessel to be pointing
      close to the target.
      This determines the midpoint of the target velocity attenuation function.
      A vector of three angles, in degrees, one for each of the pitch, roll and yaw axes.
      Defaults to 1° for each axis.

      :Attribute: Can be read or written
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: auto_tune

      Whether the rotation rate controllers PID parameters should be automatically tuned
      using the vessels moment of inertia and available torque. Defaults to ``True``.
      See :attr:`AutoPilot.time_to_peak` and :attr:`AutoPilot.overshoot`.

      :Attribute: Can be read or written
      :rtype: bool
      :Game Scenes: Flight

   .. attribute:: time_to_peak

      The target time to peak used to autotune the PID controllers.
      A vector of three times, in seconds, for each of the pitch, roll and yaw axes.
      Defaults to 3 seconds for each axis.

      :Attribute: Can be read or written
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: overshoot

      The target overshoot percentage used to autotune the PID controllers.
      A vector of three values, between 0 and 1, for each of the pitch, roll and yaw axes.
      Defaults to 0.01 for each axis.

      :Attribute: Can be read or written
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight

   .. attribute:: pitch_pid_gains

      Gains for the pitch PID controller.

      :Attribute: Can be read or written
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight


      .. note::

         When :attr:`AutoPilot.auto_tune` is true, these values are updated automatically,
         which will overwrite any manual changes.

   .. attribute:: roll_pid_gains

      Gains for the roll PID controller.

      :Attribute: Can be read or written
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight


      .. note::

         When :attr:`AutoPilot.auto_tune` is true, these values are updated automatically,
         which will overwrite any manual changes.

   .. attribute:: yaw_pid_gains

      Gains for the yaw PID controller.

      :Attribute: Can be read or written
      :rtype: tuple(float, float, float)
      :Game Scenes: Flight


      .. note::

         When :attr:`AutoPilot.auto_tune` is true, these values are updated automatically,
         which will overwrite any manual changes.