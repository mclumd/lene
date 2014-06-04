(in-package :reps)

(define-attribute-value NATURE.0
  (isa (value (nature))
       ))

(define-frame NATURE
  (isa (value (non-volitional-agent)))
  )

(define-frame NON-VOLITIONAL-AGENT
          (isa (value (abstract-object)))
  )

(define-attribute-value VERY-HOT.0
  (isa  (value (temperature-value)))
  )

(define-attribute-value HOT.0
  (isa  (value (temperature-value)))
  )

(define-attribute-value MEDIUM-TEMPERATURE.0
  (isa  (value (temperature-value)))
  )

(define-attribute-value COLD.0
  (isa  (value (temperature-value)))
  )

(define-attribute-value VERY-COLD.0
  (isa  (value (temperature-value)))
  )

(define-frame TEMPERATURE-VALUE
    (isa    (value  (physical-object-attribute-value)))
  )

(define-relation TEMPERATURE
    (isa            (value (physical-object-attribute)))
    (domain         (value (physical-object)))
    (co-domain      (value (temperature-value)))
    (slot           (value (temperature)))
    )
