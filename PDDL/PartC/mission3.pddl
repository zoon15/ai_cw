(define (problem lunar-mission-3)
    (:domain lunar-extended)

    (:objects
        w1 w2 w3 w4 w5 w6 - waypoint ;;waypoints from figure 3
        r1 r2 - rover ;;the rovers
        l1 l2 - lander ;;the landers
        alice bob - astronaut ;;two astronauts for PART 2C
    )

    (:init
        ;; roads from Figure 3 (each connected fact is one direction)
        (connected w1 w2) ;;two way road between w1 and w2
        (connected w2 w1)
        (connected w2 w3) ;; one way road from w2 to w3
        (connected w3 w5) ;;two way road between w3 and w5
        (connected w5 w3)
        (connected w2 w4) ;;two way road between w2 and w4
        (connected w4 w2)
        (connected w5 w6) ;;one way road from w5 to w6
        (connected w6 w4) ;;one way road from w6 to w4

        ;; rover 1 belongs to lander 1 and is already deployed
        (belongs r1 l1) ;;r1 is lander 1's rover
        (lander_at l1 w2) ;;lander 1 is at w2
        (at r1 w2) ;;r1 starts on the ground at w2

        ;; rover 2 belongs to lander 2 and is still aboard
        (belongs r2 l2) ;;r2 is lander 2's rover
        (lander_at l2 w1) ;;lander 2 is at w1 (waypoint is our choice as question is not specifying it)
        (undeployed r2) ;;r2 is still inside lander 2

        ;; memories, arms and lander stores all start free
        (memory_free r1) ;; both rovers can take one image or scan
        (memory_free r2)
        (arms_free r1) ;;both rovers can take one sample
        (arms_free r2)
        (store_empty l1) ;;both landers have place for one sample
        (store_empty l2)

        ;; samples on the ground
        (sample_at w5) ;;a sample is at w5
        (sample_at w1) ;;a sample is at w1

        ;; Alice crews lander 1 (docking bay), Bob crews lander 2 (control room)
        (astronaut_of alice l1) ;; alice is crew of lander 1
        (in_docking_bay alice) ;; alice is in the docking bay
        (astronaut_of bob l2) ;; bob is crew of lander 2
        (in_control_room bob) ;; bob is in the control room
            )

    (:goal
        (and
            (image_sent w3 l1) ;; image of w3 reaches lander 1
            (scan_sent w4 l2) ;; scan of w4 reaches lander 2
            (image_sent w2 l2) ;; image of w2 reaches lander 2
            (scan_sent w6 l1) ;; scan of w6 reaches lander 1
            (sample_stored w5 l1) ;; sample from w5 is stored in lander 1
            (sample_stored w1 l2) ;; sample from w1 is stored in lander 2
        )
    )
)
