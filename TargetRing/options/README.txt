Target ring spin options
========================

The active ring config is TargetIndicator.ini. To change how the ring behaves,
copy one of these over it (in the skin's folder AND in the game's uifiles\default
folder), then fully restart EverQuest (the ring is cached at launch):

  no-spin.ini    - static ring, no rotation. Loads fastest (9 textures).
  spin-slow.ini  - slow rotation.
  spin.ini       - normal rotation.
  spin-fast.ini  - fast rotation.

To fine-tune spin speed yourself: in a spinning file, 'Duration' sets how long
the 82-frame cycle takes - higher = slower spin, lower = faster. To stop spin
entirely, set FrameCount=0 and add '0' to each con Texture (e.g. Grey_ -> Grey_0).
