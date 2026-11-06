from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher

NOT_LISTED = "not listed yet"

# Starter data for the happy path. Replace/extend with your curated association
# data (check each association's own website before filling in the details).
ASSOCIATIONS: List[Dict[str, str]] = [
    {
        "name": "FC Kunde",
        "category": "sports",
        "summary": "a student football club with competitive matches, training-only membership and social activities.",
        "language": NOT_LISTED,
        "cost": NOT_LISTED,
        "how_to_join": NOT_LISTED,
        "contact": NOT_LISTED,
    },
    {
        "name": "'t Haasje",
        "category": "sports",
        "summary": "a student athletics association.",
        "language": NOT_LISTED,
        "cost": NOT_LISTED,
        "how_to_join": NOT_LISTED,
        "contact": NOT_LISTED,
    },
    {
        "name": "De Cycloop",
        "category": "creative",
        "summary": "a student photography association with photography activities, courses, workshops and social events.",
        "language": NOT_LISTED,
        "cost": NOT_LISTED,
        "how_to_join": NOT_LISTED,
        "contact": NOT_LISTED,
    },
]


class ActionFindAssociations(Action):
    def name(self) -> Text:
        return "action_find_associations"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        category = tracker.get_slot("category")
        matches = [a for a in ASSOCIATIONS if a["category"] == category]

        if not matches:
            dispatcher.utter_message(
                text=f"I don't have any {category} associations in my list yet."
            )
            return []

        lines = [f"- {a['name']}: {a['summary']}" for a in matches]
        dispatcher.utter_message(
            text=f"Here's what I've got for {category}:\n" + "\n".join(lines)
        )
        return []


class ActionAssociationDetails(Action):
    def name(self) -> Text:
        return "action_association_details"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        wanted = (tracker.get_slot("association_name") or "").strip().lower()

        match = None
        for a in ASSOCIATIONS:
            name = a["name"].lower()
            if wanted and (wanted in name or name in wanted):
                match = a
                break

        if match is None:
            dispatcher.utter_message(
                text="I couldn't find that one in my list. Which one from the list did you mean?"
            )
            return []

        dispatcher.utter_message(
            text=(
                f"{match['name']} is {match['summary']}\n"
                f"Language: {match['language']}\n"
                f"Cost: {match['cost']}\n"
                f"How to join: {match['how_to_join']}\n"
                f"Contact: {match['contact']}"
            )
        )
        return []