# v1.4 Card Economy and Zone Model

## What this document is

A location map for every physical Race card and its effect on circulation.

## How to use it

Follow transitions by card ID. Count hand, slots, attachments and staged cards separately; never treat a zone as another hand.

## Key takeaways

Six-card maximum and one draw allow hands to shrink. Installed cards become delayed Effort; attached cards cannot move and remain locked until complete Condition removal.

## Action and play budgets are separate from card location

Each runner turn offers **one Treat/Prepare** opportunity and **up to two Race-card plays**. Playing a **new hand card** through Treat/Prepare for Training/Gear installation or replacement, Fuel Effect, or Condition remedy/attachment spends **both** one Treat/Prepare and one card play. Its printed Effort is unused. Legal relocation of already-equipped Gear or an assistance request spends Treat/Prepare but **zero new card plays**. Eligible Direct Slot Movement spends **one card play and zero Treat/Prepare**. These budgets govern transitions, but a card's current zone determines whether it can make a transition at all.

## Where cards live

The **Race draw pile** holds undrawn cards; a **runner hand** holds concealed normal cards; two **Training slots** and two normal **Gear slots** hold installed cards; a **Condition attachment** holds compatible treatment Gear outside normal slots. During an action a card is in **Movement** or **Effect resolution**, then enters **Race discard** unless its Effect persists. A staged Event stays in its timed zone until expiration. A **reshuffled draw pile** is formed solely from eligible discard when needed. Condition cards revealed on draw immediately enter the active Condition zone instead of hand; removed Conditions discard. Each physical card has one location at a time.

| Legal transition | Trigger | Budget / consequence |
|---|---|---|
| Draw pile → hand | One normal Replenish draw below six, or valid other draw | Conditions encountered auto-enter play and cause replacement of the normal draw. |
| Hand → Movement → discard | Choose MOVEMENT mode | Printed Effort, normal Movement Energy, one of two plays. |
| Hand → Training slot | Treat/Prepare installation | One Treat/Prepare and one of two card plays; Effect starts; age starts now. |
| Hand → Gear slot | Treat/Prepare equipment | Same two budgets; at most two equipped, one footwear (`is_footwear` true). Broad categories are descriptive only. |
| Slot → Direct Slot Movement → discard | Continuously installed for two full runner turns | No Treat/Prepare; Effect ends before payment and calculation; one card play. |
| Slot → discard; hand → same slot | Treat/Prepare replacement | Old never enters hand, new clock starts at zero. |
| Hand → Condition attachment | Compatible Gear treatment | One Treat/Prepare and one card play; committed outside normal Gear slots. |
| Equipped Gear → Condition attachment | Legal relocation | Treat/Prepare but no newly played card; equipped Effect ends. |
| Condition attachment → discard | That Condition is completely removed | All attached cards discard, even at a station. Partial treatment or persistent zero retains them. |
| Hand ↔ another active runner’s hand | Stranded one-for-one assistance | Requester’s Treat/Prepare, no Race-card play; helper owes no action. |
| Hand → Event resolution → discard / staged zone | Movement-phase Event Effect | One play and one Event limit; no Effort. Staged resolves/expires then discards. |
| Hand → Fuel Effect → discard | Treat/Prepare | +2 Energy **or** printed remedy if legal; no Effort. |
| Discard → reshuffled draw pile | Draw demanded when draw pile empty | Exclude all hands, slots, attachments, active Conditions and staged cards. |

**Forbidden transitions:** Condition attachment → Movement, hand, normal slot, assistance, or another Condition; a replaced card → hand; newly installed or one-turn-old slot → Direct Slot Movement; a slot → hand merely because hand is empty; installed/attached/staged card → deck reshuffle; a Fuel Effect blocked by Nausea → recovery; Effect and printed Effort from the same card play. No zone produces an extra card when draw and eligible discard are empty.

## Why circulation changes

At six cards each, opening hands remove 24 cards from the shared 108-card supply with four runners, 48 with eight, and 72 with twelve before Conditions/replacement and pre-race exchanges. These are upper bounds for initially held normal cards, not guaranteed remaining pile sizes: Condition chains and exchanges alter draws. Installed Training/Gear and attachments further reduce the cards available for reshuffle; sacrifice returns a slotted card to discard after Movement; complete Condition removal releases attachments into discard, never directly into hand. Track deck exhaustion, hand size, time held installed, attachment duration, and reshuffle frequency before deciding whether the economy is too tight.
