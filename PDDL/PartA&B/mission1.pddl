(define (problem lunar-mission-1)
    (:domain lunar)

;;these are the specifications for mission 1 
    (:objects 
        rover1 - rover ;; the rover
        lander1 - lander ;; the lander
        wp1 wp2 wp3 wp4 wp5 - waypoint ;; waypoints from figure 2
    )

    (:init
        (lander_at lander1 wp1)  ;; lander lands at wp1 (wp1 is our choice since start point is not specified)
        (store_empty lander1) ;; lander 1 has place for one sample

        ;; the rover
        (belongs rover1 lander1) ;; rover1 is lander 1's rover
        (undeployed rover1) ;; rover1 is still inside the lander
        (memory_free rover1) ;; rover1 can take one image or scan
        (arms_free rover1) ;; rover1 can carry one sample

        ;; samples on the ground
        (sample_at wp1) ;; a sample is at wp1

        ;; roads from Figure 2 (each connected fact is one direction)
        (connected wp1 wp2)
        (connected wp2 wp3)
        (connected wp1 wp4)
        (connected wp4 wp3)
        (connected wp3 wp5)
        (connected wp5 wp1)
    )

    ;; mission goals: data must be sent to the lander and the sample must be stored in it
    (:goal
        (and
            (image_sent wp5 lander1) ;; image of wp5 reaches lander 1
            (scan_sent wp3 lander1) ;; scan of wp3 reaches lander 1
            (sample_stored wp1 lander1) ;; sample from wp1 is stored in lander 1
        )
    )
)
