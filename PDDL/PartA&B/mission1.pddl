(define (problem lunar-mission-1)
    (:domain lunar)

;;these are the specifications for mission1 
    (:objects 
        rover1  - rover
        lander1 - lander
        wp1 wp2 wp3 wp4 wp5 - waypoint
    )

    (:init
        (lander_at lander1 wp1)  ;; lander lands at wp1
        (store_empty lander1) ;; The lander's sample store starts empty (room for one sample)

        
        ;; rover1 belongs to lander1 (it can only deploy from or report to it)
        (belongs rover1 lander1)
        ;; rover1 starts aboard the lander, so there is NO (at rover1 ...)
        ;; fact; the deploy action will place it at wp1.
        (undeployed rover1)
        ;; Memory starts empty, so it can take one image or scan.
        (memory_free rover1)
        ;; Arms start empty, so it can pick up one sample.
        (arms_free rover1)

        ;; ---- Samples ----
        ;; There is a sample to collect at wp1.
        (sample_at wp1)

        ;; ---- Roads (Figure 2) ----
        ;; Every road is ONE-WAY, so each has exactly one connected fact.
        (connected wp1 wp2)
        (connected wp2 wp3)
        (connected wp1 wp4)
        (connected wp4 wp3)
        (connected wp3 wp5)
        (connected wp5 wp1)
    )

    ;; Mission goals. Taking data is not enough: it must be SENT to the
    ;; lander, and the sample must be STORED in the lander.
    (:goal (and
        (image_sent wp5 lander1)
        (scan_sent wp3 lander1)
        (sample_stored wp1 lander1)
    ))
)
