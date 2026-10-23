(define (domain lunar)
    (:requirements :strips :typing)
    ; Types has the kind of things that exist 
    (:types
       lander 
       rover 
       waypoint
    )
    ; Predicates holds true or false statements about it 
    (:predicates
    ;; Tells the location of the rover and lander
      (at ?r - rover ?w - waypoint) ;; ?r rover is at the waypoint ?w
      (connected ?w1 - waypoint ?w2 - waypoint) ;; connection from ?w1 to ?w2 
      (belongs ?r - rover ?l - lander) ;; ?r rover belongs to lander ?l
      (lander_at ?l - lander ?w - waypoint) ;; ?l lander is at waypoint ?w
      
      ;; state of the rover 
      (undeployed ?r - rover) ;; the rover is still aboard the lander 
      (memory_free ?r - rover) ;; rover can take new images and scans 
      (arms_free ?r - rover) ;; rover doesnt have a sample 
      
      ;; state of the lander 
      (store_empty ?l - lander) ;; the lander has space for a sample 
      
      ;; items in the environment
      (sample_at ?w - waypoint) ;; the uncollected sample is at ?w waypoint 
      (has_image ?r - rover ?w - waypoint) ;; the rover holds an unsent image 
      (has_scan ?r - rover ?w - waypoint) ;; the rover holds an unsent scan 
      
      ;; goals notes of the missions 
     (image_sent ?w - waypoint ?l - lander) ;; image of ?w has reached lander 
     (scan_sent ?w - waypoint ?l - lander) ;; scan of ?w has reached lander 
     (sample_stored ?w - waypoint ?l - lander) ;; the sample fron ?w is stored at lander 

     (carrying ?r - rover ?w - waypoint) ;; holds the sample that the rover picked up at the waypoint 
    )

    ;;Actions holds the moves that need to be done 
    ;;the rover that's undeployed gets placed on the ground at lander’s location
    (:action deploy
        :parameters (?r - rover ?w - waypoint ?l - lander)
        :precondition (and
            (undeployed ?r ) ;; the rover is still aboard 
            (belongs ?r ?l) ;; the lander should be rover's own lander 
            (lander_at ?l ?w) ;; where the lander is located 
        )
        :effect (and
            (at ?r ?w) ;; rover is on the ground 
            (not (undeployed ?r)) ;; the rover isnt aboard anymore 
        )
    )
    ;; the rover drives from one waypoint to its connected waypoint 
    (:action move 
        :parameters (?r - rover ?from - waypoint ?to - waypoint )
        :precondition (and
            (at ?r ?from) ;; rover is at the start 
            (connected ?from ?to) ;; it goes from ?from to ?to 
        )
        :effect (and
            (at ?r ?to) ;; rover is at the new waypoint 
            (not (at ?r ?from)) ;; its not at the old one anymore
        )
    )
    ;; the rover takes an image of the waypoint it is at 
    (:action take_image
        :parameters (?r - rover ?w - waypoint )
        :precondition (and
            (at ?r ?w) ;; rover is at its waypoint 
            (memory_free ?r) ;; memory is not full 
        )
        :effect (and
            (has_image ?r ?w) ;; rover holds the image now  
            (not (memory_free ?r)) ;; memory is full 
        )
    )
    ;; the rover takes a scan of the waypoint it is at 
    (:action take_scan
        :parameters (?r - rover ?w - waypoint )
        :precondition (and
            (at ?r ?w) ;; rover is at the waypoint  
            (memory_free ?r) ;; memory is not full
        )
        :effect (and
            (has_scan ?r ?w) ;; rover holds the scan now  
            (not (memory_free ?r)) ;; memory is full 
        )
    )
    
    ;; the rover sends an image it holds to its own lander 
    (:action transmit_image
        :parameters (?r - rover ?w - waypoint ?l - lander)
        :precondition (and
            (has_image ?r ?w) ;; rover should have an image of ?w
            (belongs ?r ?l) ;; the lander should be rover's own lander 
        )
        :effect (and
            (image_sent ?w ?l) ;; goal note is true 
            (not (has_image ?r ?w)) ;; rover doesnt have the image 
            (memory_free ?r) ;; memory is free 
        )
    )
    ;; the rover sends a scan it holds to its own lander 
    (:action transmit_scan
        :parameters (?r - rover ?w - waypoint ?l - lander)
        :precondition (and
            (has_scan ?r ?w) ;; rover should have the scan 
            (belongs ?r ?l) ;; the scan should be rover's own 
        )
        :effect (and
            (scan_sent ?w ?l) ;; goal note is true 
            (not (has_scan ?r ?w)) ;; rover doesnt have the scan anymore 
            (memory_free ?r) ;; memory is free now 
        )
    )
    ;; the rover picks up the sample at its current waypoint 
    (:action collect_sample
        :parameters (?r - rover ?w - waypoint )
        :precondition (and
            (at ?r ?w) ;; rover is at the waypoint  
            (sample_at ?w) ;; location of the sample to pick up 
            (arms_free ?r) ;; the arms are empty
        )
        :effect (and
            (carrying ?r ?w) ;; the sample from ?w is now held by the rover 
            (not (sample_at ?w)) ;; the sample isnt at the ground anymore 
            (not (arms_free ?r))  ;; the arms are full 
        )
    )
    ;; the rover drops the sample into its own lander 
    (:action store_sample
        :parameters (?r - rover ?w - waypoint ?l - lander ?lw - waypoint )
        :precondition (and
            (carrying ?r ?w) ;; rover should hold that sample   
            (belongs ?r ?l) ;; the lander should be rover's own 
            (lander_at ?l ?lw) ;; the location of the lander 
            (at ?r ?lw) ;; rover should go to the lander 
            (store_empty ?l) ;; lander has room for the sample 
        )
        :effect (and
            (sample_stored ?w ?l) ;; the goal note is true 
            (not (carrying ?r ?w)) ;; rover no longer has the sample 
            (arms_free ?r)  ;; the arms are free again 
            ( not(store_empty ?l)) ;; the lander's store is now full 
        )
    )
    

    

)
