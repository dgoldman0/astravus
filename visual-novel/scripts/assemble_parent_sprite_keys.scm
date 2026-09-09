; Native GIMP assembly for the accepted parent visual keys.
; Run from visual-novel via art/character-keys/run-parent-sprite-gimp.sh.
; All color and anatomy comes from the generated edit or immutable original.
; GIMP supplies editable feathered masks and the final composition.

(define (parent-path name file)
  (string-append "art/character-keys/" name "/" file))

(define (parent-save-png image drawable path)
  (file-png-save2 RUN-NONINTERACTIVE image drawable path path
    0 9 0 0 0 0 0 0 0))

(define (parent-save-flat image path)
  (let* ((copy (car (gimp-image-duplicate image)))
         (flat (car (gimp-image-flatten copy))))
    (parent-save-png copy flat path)
    (gimp-image-delete copy)))

(define (parent-layer image name title adds subtracts mask-file)
  (let* ((layer (car (gimp-file-load-layer RUN-NONINTERACTIVE image
                       (parent-path name "sprite-generated.png"))))
         (mask 0) (mi 0) (ml 0))
    (gimp-image-insert-layer image layer 0 0)
    (gimp-item-set-name layer title)
    (gimp-layer-set-mode layer 0)
    (gimp-layer-set-offsets layer 0 0)
    (gimp-selection-none image)
    (for-each (lambda (points)
      (gimp-image-select-polygon image 0 (vector-length points) points)) adds)
    (for-each (lambda (points)
      (gimp-image-select-polygon image 1 (vector-length points) points)) subtracts)
    (gimp-selection-feather image 2.0)
    (set! mask (car (gimp-layer-create-mask layer 4)))
    (gimp-layer-add-mask layer mask)
    (gimp-selection-none image)
    (set! mi (car (gimp-image-new (car (gimp-image-width image))
                                (car (gimp-image-height image)) GRAY)))
    (set! ml (car (gimp-layer-new-from-drawable mask mi)))
    (gimp-image-insert-layer mi ml 0 0)
    (parent-save-png mi ml (parent-path name mask-file))
    (gimp-image-delete mi)
    layer))

(define (parent-finish image base name)
  (let* ((active (car (gimp-image-get-active-layer image)))
         (reopened 0) (layers 0) (index 0) (layer 0))
    (gimp-xcf-save RUN-NONINTERACTIVE image active
      (parent-path name "sprite-refined.xcf") (parent-path name "sprite-refined.xcf"))
    (parent-save-flat image (parent-path name "sprite-refined.png"))
    (gimp-image-delete image)
    (set! reopened (car (gimp-file-load RUN-NONINTERACTIVE
      (parent-path name "sprite-refined.xcf") (parent-path name "sprite-refined.xcf"))))
    (parent-save-flat reopened (string-append audit-dir "/" name "-reopened.png"))
    (set! layers (gimp-image-get-layers reopened))
    (while (< index (car layers))
      (set! layer (vector-ref (cadr layers) index))
      (if (= (car (gimp-item-get-lock-content layer)) FALSE)
        (gimp-item-set-visible layer FALSE))
      (set! index (+ index 1)))
    (parent-save-flat reopened (string-append audit-dir "/" name "-restored.png"))
    (gimp-image-delete reopened)))

(gimp-context-push)
(gimp-context-set-antialias TRUE)
(gimp-context-set-feather FALSE)

(let* ((name "arin")
       (path (parent-path name "sprite-before.png"))
       (image (car (gimp-file-load RUN-NONINTERACTIVE path path)))
       (base (car (gimp-image-get-active-layer image))))
  (gimp-item-set-name base "Original Arin sprite — immutable base")
  (gimp-item-set-lock-content base TRUE)
  (parent-layer image name "Arin — pale freckled face, blue eyes and cropped auburn hair"
    (list (vector
      405.0 4.0 626.0 4.0 634.0 97.0 619.0 153.0
      592.0 196.0 558.0 226.0 543.0 253.0 549.0 292.0
      552.0 334.0 531.0 314.0 508.0 282.0 482.0 267.0
      462.0 245.0 440.0 238.0 438.0 216.0 454.0 189.0
      435.0 166.0 416.0 137.0))
    (list) "mask-head.png")
  (parent-layer image name "Arin — consistent pale forearms and hands"
    (list
      (vector
        309.0 525.0 349.0 519.0 378.0 536.0 383.0 584.0
        386.0 636.0 391.0 689.0 396.0 724.0 413.0 762.0
        421.0 815.0 408.0 835.0 384.0 827.0 354.0 807.0
        342.0 782.0 341.0 734.0 331.0 676.0 317.0 604.0)
      (vector
        631.0 502.0 654.0 501.0 674.0 532.0 674.0 572.0
        668.0 607.0 654.0 637.0 632.0 651.0 608.0 645.0
        593.0 633.0 606.0 616.0 611.0 602.0 597.0 606.0
        588.0 596.0 608.0 578.0 629.0 568.0 629.0 541.0))
    (list) "mask-arms.png")
  (parent-finish image base name))

(let* ((name "sage")
       (path (parent-path name "sprite-before.png"))
       (image (car (gimp-file-load RUN-NONINTERACTIVE path path)))
       (base (car (gimp-image-get-active-layer image))))
  (gimp-item-set-name base "Original Sage sprite — immutable base")
  (gimp-item-set-lock-content base TRUE)
  (parent-layer image name "Sage — rounded face, gray eyes and swept sandy crop"
    (list (vector
      402.0 24.0 623.0 23.0 641.0 111.0 626.0 191.0
      607.0 241.0 626.0 275.0 606.0 316.0 566.0 368.0
      527.0 413.0 505.0 400.0 500.0 356.0 489.0 308.0
      469.0 268.0 443.0 229.0 417.0 180.0 400.0 129.0))
    (list) "mask-head.png")
  (parent-layer image name "Sage — medium shoulder and torso build, same tunic"
    (list (vector
      478.0 263.0 502.0 292.0 510.0 354.0 520.0 418.0
      541.0 400.0 583.0 345.0 615.0 294.0 622.0 266.0
      663.0 278.0 711.0 300.0 735.0 344.0 742.0 403.0
      735.0 470.0 716.0 526.0 700.0 584.0 691.0 649.0
      698.0 712.0 713.0 780.0 736.0 848.0 694.0 867.0
      646.0 850.0 598.0 872.0 537.0 877.0 477.0 864.0
      420.0 852.0 373.0 836.0 351.0 810.0 371.0 738.0
      389.0 659.0 357.0 624.0 347.0 562.0 356.0 499.0
      367.0 434.0 376.0 370.0 397.0 321.0 435.0 287.0))
    (list (vector
      387.0 578.0 424.0 568.0 449.0 593.0 464.0 629.0
      504.0 621.0 556.0 592.0 584.0 585.0 611.0 610.0
      617.0 638.0 581.0 663.0 537.0 690.0 514.0 724.0
      537.0 783.0 520.0 799.0 482.0 793.0 453.0 778.0
      429.0 753.0 423.0 724.0 400.0 722.0 391.0 701.0
      401.0 666.0 396.0 633.0))
    "mask-torso.png")
  (parent-finish image base name))

(gimp-context-pop)
