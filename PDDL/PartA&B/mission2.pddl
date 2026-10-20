(define (problem lunar-mission-2)
    (:domain lunar)

    (:objects
        w1 w2 w3 w4 w5 w6 - waypoint ;; these are the waypoints from the figure 
        r1 r2 - rover ;; the rovers 
        l1 l2 - lander ;; the landers   
    )

    (:init
        ;; two way connection from w1 to w2 and w2 to w1
        (connected w1 w2) 
        (connected w2 w1)
        (connected w2 w3) ;;one way connection from w2 to w3
        ;; two way connection from w3 to w5 and w5 to w3
        (connected w3 w5) 
        (connected w5 w3)
        ;; two way connection from w2 to w4 and from w4 to w2
        (connected w2 w4)
        (connected w4 w2)
        ;; one way connection from w5 to w6 
        (connected w5 w6)
        ;; one way connection from w6 to w4 
        (connected w6 w4)

        ;; rover 1 belongs to lander 1 and has been deployed 
        (belongs r1 l1)
        (lander_at l1 w2)
        (at r1 w2)

        ;; rover 2 belongs to lander 2 but hasnt been deployed yet 
        (belongs r2 l2)
        (lander_at l2 w1)
        (undeployed r2)

        ;; everything is free 
        (memory_free r1)
        (memory_free r2)
        (arms_free r1)
        (arms_free r2)
        (store_empty l1)
        (store_empty l2)

        ;; the samples exist 
        (sample_at w5)
        (sample_at w1)   
    )

    (:goal
        (and
           (image_sent w3 l1)
           (scan_sent w4 l2)
           (image_sent w2 l2)
           (scan_sent w6 l1)
           (sample_stored w5 l1)
           (sample_stored w1 l2)
        )
    )
)