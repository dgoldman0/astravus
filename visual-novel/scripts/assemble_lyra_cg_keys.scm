; Run from visual-novel. Native GIMP 2.10 composition; no full-frame resampling.
; The full generated scenes are paint donors, never replacement backgrounds.
(define pass-dir "../development/visual-novel/art/character-refinements/")
(define (pass-path name suffix) (string-append pass-dir name suffix))
(define (pass-png image layer path)
  (file-png-save2 RUN-NONINTERACTIVE image layer path path 0 9 0 0 0 0 0 0 0))
(define (pass-flat image path)
  (let* ((copy (car (gimp-image-duplicate image)))
         (flat (car (gimp-image-flatten copy))))
    (pass-png copy flat path)
    (gimp-image-delete copy)))
(define (refine-lyra name points)
  (let* ((path (pass-path name "-original.png"))
         (image (car (gimp-file-load RUN-NONINTERACTIVE path path)))
         (base (car (gimp-image-get-active-layer image)))
         (layer (car (gimp-file-load-layer RUN-NONINTERACTIVE image
                   (pass-path name "-generated.png"))))
         (mask 0) (mask-image 0) (mask-layer 0) (reopened 0) (layers 0))
    (gimp-item-set-name base "Original scene — locked")
    (gimp-item-set-lock-content base TRUE)
    (gimp-image-insert-layer image layer 0 0)
    (gimp-item-set-name layer "Lyra — facial construction, original scene performance")
    (gimp-layer-set-mode layer 0)
    (gimp-layer-set-offsets layer 0 0)
    (gimp-image-select-polygon image CHANNEL-OP-REPLACE (vector-length points) points)
    (gimp-selection-feather image 3.0)
    (set! mask (car (gimp-layer-create-mask layer ADD-SELECTION-MASK)))
    (gimp-layer-add-mask layer mask)
    (gimp-selection-none image)
    (set! mask-image (car (gimp-image-new 1672 941 GRAY)))
    (set! mask-layer (car (gimp-layer-new-from-drawable mask mask-image)))
    (gimp-image-insert-layer mask-image mask-layer 0 0)
    (pass-png mask-image mask-layer (pass-path name "-mask.png"))
    (gimp-image-delete mask-image)
    (gimp-xcf-save RUN-NONINTERACTIVE image layer
      (pass-path name "-refined.xcf") (pass-path name "-refined.xcf"))
    (pass-flat image (pass-path name "-refined.png"))
    (gimp-image-delete image)
    (set! reopened (car (gimp-file-load RUN-NONINTERACTIVE
      (pass-path name "-refined.xcf") (pass-path name "-refined.xcf"))))
    (pass-flat reopened (string-append audit-dir "/" name "-reopened.png"))
    (set! layers (gimp-image-get-layers reopened))
    (gimp-item-set-visible (vector-ref (cadr layers) 0) FALSE)
    (pass-flat reopened (string-append audit-dir "/" name "-restored.png"))
    (gimp-image-delete reopened)))
(gimp-context-push)
(gimp-context-set-antialias TRUE)
(gimp-context-set-feather FALSE)
(refine-lyra "pond-rescue" (vector
  1054 449 1071 444 1087 451 1100 467 1109 485 1115 509
  1120 529 1111 544 1093 554 1070 551 1052 541 1039 528
  1037 508 1043 487 1043 468))
(refine-lyra "pond-comfort" (vector
  786 351 805 345 829 344 850 352 868 365 880 383
  885 409 887 433 876 450 858 464 837 470 816 463
  796 451 782 435 776 413 775 390 779 368))
(refine-lyra "theme-insect-discovery" (vector
  1046 326 1081 323 1114 341 1138 364 1155 393 1174 422
  1193 447 1202 476 1204 509 1190 540 1166 560 1139 578
  1110 590 1082 586 1058 574 1035 554 1017 530 1005 504
  997 475 998 446 1009 418 1017 388 1028 356))
(gimp-context-pop)
