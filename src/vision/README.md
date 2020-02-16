# Computer vision

Documentation to follow...

## Mussels task TODO: Refactor later

Example code:
```python
    img = _cv2.imread('./catch.PNG')
    _orig, _circles_removed, _blurred_and_smoothed, _convex_hull, _mussels_found, _mussels_count = count_mussels(img)
    _cv2.imshow("1. Original", _orig)
    _cv2.imshow("2. Circles removed", _circles_removed)
    _cv2.imshow("3. Blurred and smoothed", _blurred_and_smoothed)
    _cv2.imshow("4. Convex hull", _convex_hull)
    _cv2.imshow("5. Mussels", _mussels_found)
    print("Counted", _mussels_count, "mussels")
    _cv2.waitKey(0)
```