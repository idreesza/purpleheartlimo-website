/* DOM-free vehicle carousel state transitions shared by the booking pages. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.PHLVehicleState = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function toggleExpanded(state) {
    state = state || {};
    return {
      selectedId: state.selectedId || null,
      expanded: !!state.selectedId && !state.expanded
    };
  }

  function nextVehicleIndex(index, count, direction) {
    count = Number(count);
    if (!Number.isFinite(count) || count < 1) return -1;
    count = Math.floor(count);
    index = Number.isFinite(Number(index)) ? Math.trunc(Number(index)) : 0;
    direction = Number(direction) < 0 ? -1 : 1;
    return (index + direction + count) % count;
  }

  /*
   * The collapsed carousel deliberately has variable-width slides: the
   * selected vehicle keeps its normal card width while its neighbours become
   * thumbnails. Keep this mapping DOM-free so both localized pages can use
   * the same state contract and tests can verify it without a browser.
   */
  function vehiclePresentation(vehicleIds, selectedId, expanded) {
    var ids = Array.isArray(vehicleIds) ? vehicleIds.map(function (vehicle) {
      return vehicle && typeof vehicle === 'object' ? vehicle.id : vehicle;
    }) : [];
    var selectedIndex = ids.indexOf(selectedId);
    var hasSelection = selectedIndex >= 0;
    var mode = !hasSelection ? 'initial' : (expanded ? 'expanded' : 'collapsed');

    return {
      mode: mode,
      selectedId: hasSelection ? selectedId : null,
      selectedIndex: hasSelection ? selectedIndex : -1,
      cards: ids.map(function (id) {
        var selected = hasSelection && id === selectedId;
        return {
          id: id,
          selected: selected,
          size: mode === 'collapsed' && !selected ? 'thumbnail' : 'full'
        };
      })
    };
  }

  function selectedScrollTarget(slideLeft, trackLeft) {
    slideLeft = Number(slideLeft);
    trackLeft = Number(trackLeft);
    if (!Number.isFinite(slideLeft) || !Number.isFinite(trackLeft)) return 0;
    return Math.max(0, slideLeft - trackLeft);
  }

  return {
    toggleExpanded,
    nextVehicleIndex,
    vehiclePresentation,
    selectedScrollTarget
  };
}));