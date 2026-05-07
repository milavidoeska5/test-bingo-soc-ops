# UI Design Spec

## Iteration 1: Card Deck Shuffle Mode

### Goal
Introduce a new game mode where players draw one random social question at a time from a virtual deck and can rapidly get the next prompt with a tactile flip interaction.

### UX Decisions
- Added a third mode selector: Card Deck Shuffle.
- Reused the existing mission start flow to keep mode-switching friction low.
- In active play, the mode shows one large, central card to focus attention on the current prompt.
- The card is also the control surface: tapping it requests the next random question.
- Added a visible draw counter to reinforce momentum and progression.

### Visual Direction
- Preserved the established galaxy/glass style tokens and palette.
- Added a dedicated 3D card scene with perspective and preserved 3D transform stack.
- Front face emphasizes action (Tap to Shuffle + star icon).
- Back face emphasizes content (random question text) with high readability.

### Motion Design
- Flip transition: rotateY with custom cubic-bezier easing.
- Star pulse adds ambient liveliness while idle.
- Press state slightly scales card while preserving the flip illusion.

### Responsiveness
- Card fills available width up to a max panel size.
- Mobile breakpoint reduces card height and question type size for legibility.

### Technical Notes
- New mode enum: card_deck_shuffle.
- Session stores a shuffled deck, current prompt text, draw count, and flip state toggle.
- New HTMX endpoint: POST /shuffle/next returns refreshed game screen.
- Deck auto-rebuilds when exhausted to allow continuous play.
