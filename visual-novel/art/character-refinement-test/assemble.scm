; Run from the visual-novel directory with run-gimp-test.sh.
; All paint comes from the original image or the generated candidate.
; GIMP creates the hand-traced feathered masks and performs composition.

(define test-folder "art/character-refinement-test/")
(define (test-path name) (string-append test-folder name))

(define (save-png image drawable path)
  (file-png-save2 RUN-NONINTERACTIVE image drawable path path
    0 9 0 0 0 0 0 0 0))

(define (save-flat image path)
  (let* ((copy (car (gimp-image-duplicate image)))
         (flat (car (gimp-image-flatten copy))))
    (save-png copy flat path)
    (gimp-image-delete copy)))

(define (select-polygon image operation coords)
  (gimp-image-select-polygon image operation (vector-length coords) coords))

(define (insert-masked-candidate image title polygons mask-file)
  (let* ((layer (car (gimp-file-load-layer RUN-NONINTERACTIVE image
                      (test-path "opening-generated-v1.png"))))
         (mask 0) (mask-image 0) (mask-layer 0))
    (gimp-image-insert-layer image layer 0 0)
    (gimp-item-set-name layer title)
    (gimp-layer-set-mode layer 0)
    (gimp-layer-set-offsets layer 0 0)
    (gimp-selection-none image)
    (for-each (lambda (points) (select-polygon image 0 points)) polygons)
    (gimp-selection-feather image 4.0)
    (set! mask (car (gimp-layer-create-mask layer 4)))
    (gimp-layer-add-mask layer mask)
    (gimp-selection-none image)

    ; Export the actual native layer mask, including its feather support.
    (set! mask-image (car (gimp-image-new 1672 941 GRAY)))
    (set! mask-layer (car (gimp-layer-new-from-drawable mask mask-image)))
    (gimp-image-insert-layer mask-image mask-layer 0 0)
    (gimp-layer-set-offsets mask-layer 0 0)
    (save-png mask-image mask-layer (test-path mask-file))
    (gimp-image-delete mask-image)
    layer))

(let* ((original "game/images/cg/first-memory-young.png")
       (image (car (gimp-file-load RUN-NONINTERACTIVE original original)))
       (base (car (gimp-image-get-active-layer image)))
       (arin-head 0) (arin-arms 0) (sage 0)
       (reopened 0) (layers 0) (index 0) (layer 0))
  (gimp-context-push)
  (gimp-context-set-antialias TRUE)
  (gimp-context-set-feather FALSE)
  (gimp-image-undo-disable image)
  (gimp-item-set-name base "Original opening painting — locked")
  (gimp-item-set-lock-content base TRUE)

  ; The head boundary follows the union of the two hair silhouettes.
  ; Small surrounding areas allow removal of the original hair fringe.
  (set! arin-head (insert-masked-candidate image
    "Arin — auburn crop, pale freckled face and neck"
    (list (vector
      332.0 237.0 344.0 207.0 370.0 177.0 395.0 152.0
      432.0 143.0 465.0 142.0 500.0 148.0 537.0 171.0
      570.0 194.0 590.0 224.0 603.0 250.0 604.0 276.0
      588.0 299.0 569.0 319.0 562.0 340.0 566.0 367.0
      551.0 385.0 535.0 404.0 514.0 409.0 488.0 399.0
      461.0 385.0 435.0 410.0 418.0 446.0 406.0 479.0
      397.0 499.0 389.0 491.0 380.0 457.0 367.0 417.0
      352.0 378.0 341.0 349.0 347.0 333.0 361.0 320.0
      352.0 296.0 337.0 276.0))
    "mask-arin-head.png"))

  (set! arin-arms (insert-masked-candidate image
    "Arin — matching pale forearms and resting hand"
    (list
      (vector
        440.0 630.0 454.0 622.0 471.0 625.0 488.0 639.0
        502.0 665.0 515.0 704.0 521.0 724.0 499.0 729.0
        477.0 717.0 460.0 703.0 449.0 675.0)
      (vector
        386.0 688.0 410.0 694.0 440.0 702.0 471.0 710.0
        508.0 713.0 547.0 715.0 578.0 727.0 600.0 747.0
        613.0 770.0 624.0 799.0 620.0 820.0 608.0 837.0
        598.0 840.0 593.0 828.0 591.0 808.0 585.0 790.0
        569.0 772.0 548.0 764.0 514.0 763.0 480.0 761.0
        446.0 758.0 414.0 754.0 393.0 748.0))
    "mask-arin-arms.png"))

  ; Sage's source hands, forearms, trousers, and the shared blanket remain.
  ; The lower edge follows the sleeve and vest above the resting forearm.
  (set! sage (insert-masked-candidate image
    "Sage — sandy crop, round face and medium upper build"
    (list (vector
      1181.0 199.0 1203.0 181.0 1234.0 171.0 1270.0 164.0
      1301.0 162.0 1336.0 172.0 1361.0 191.0 1382.0 204.0
      1401.0 231.0 1412.0 255.0 1407.0 287.0 1408.0 310.0
      1419.0 336.0 1443.0 346.0 1471.0 355.0 1503.0 376.0
      1534.0 402.0 1561.0 439.0 1581.0 478.0 1597.0 520.0
      1612.0 566.0 1620.0 603.0 1613.0 640.0 1600.0 667.0
      1573.0 686.0 1543.0 698.0 1512.0 710.0 1488.0 724.0
      1457.0 731.0 1428.0 731.0 1397.0 725.0 1373.0 713.0
      1350.0 700.0 1340.0 678.0 1344.0 657.0 1348.0 646.0
      1304.0 653.0 1278.0 653.0 1255.0 628.0 1243.0 612.0
      1225.0 599.0 1205.0 590.0 1184.0 588.0 1164.0 596.0
      1150.0 593.0 1152.0 572.0 1165.0 547.0 1181.0 514.0
      1194.0 479.0 1205.0 446.0 1220.0 416.0 1225.0 394.0
      1209.0 376.0 1202.0 366.0 1215.0 355.0 1218.0 343.0
      1202.0 334.0 1199.0 320.0 1183.0 311.0 1174.0 292.0
      1171.0 270.0 1174.0 247.0 1173.0 226.0))
    "mask-sage.png"))

  (gimp-image-undo-enable image)
  (gimp-image-set-active-layer image sage)
  (gimp-xcf-save RUN-NONINTERACTIVE image sage
    (test-path "opening-refined-v1.xcf") (test-path "opening-refined-v1.xcf"))
  (save-flat image (test-path "opening-refined-v1.png"))
  (gimp-image-delete image)

  ; Reopen the saved XCF and independently export both composite and base.
  (set! reopened (car (gimp-file-load RUN-NONINTERACTIVE
    (test-path "opening-refined-v1.xcf") (test-path "opening-refined-v1.xcf"))))
  (save-flat reopened (string-append audit-dir "/reopened-output.png"))
  (set! layers (gimp-image-get-layers reopened))
  (while (< index (car layers))
    (set! layer (vector-ref (cadr layers) index))
    (if (= (car (gimp-item-get-lock-content layer)) FALSE)
      (gimp-item-set-visible layer FALSE))
    (set! index (+ index 1)))
  (save-flat reopened (string-append audit-dir "/restored-base.png"))
  (gimp-image-delete reopened)
  (gimp-context-pop))
