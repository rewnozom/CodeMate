import unittest
import asyncio
from uuid import UUID
from cmate.core.event_bus import EventBus, EventPriority, EventCategory

class TestEventBus(unittest.TestCase):
    def setUp(self):
        self.event_bus = EventBus()
        # Create a new event loop and store it for use in tests.
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.event_bus.start())

    def tearDown(self):
        # Stop the event bus on the same loop and then close it.
        self.loop.run_until_complete(self.event_bus.stop())
        self.loop.close()

    def test_publish_and_subscribe(self):
        events = []

        def handler(event):
            events.append(event)

        subscription_id = self.event_bus.subscribe("test_event", handler, priority=EventPriority.HIGH)
        self.assertIsInstance(subscription_id, UUID)
        self.loop.run_until_complete(
            self.event_bus.publish("test_event", {"message": "Hello"},
                                     priority=EventPriority.HIGH,
                                     category=EventCategory.USER)
        )
        self.loop.run_until_complete(asyncio.sleep(0.2))
        self.assertGreater(len(events), 0)
        for event in events:
            self.assertEqual(event.get("priority"), EventPriority.HIGH)

    def test_unsubscribe(self):
        events = []

        def handler(event):
            events.append(event)

        subscription_id = self.event_bus.subscribe("test_event", handler)
        unsubscribed = self.event_bus.unsubscribe(subscription_id)
        self.assertTrue(unsubscribed)
        self.loop.run_until_complete(
            self.event_bus.publish("test_event", {"message": "After unsubscribe"})
        )
        self.loop.run_until_complete(asyncio.sleep(0.2))
        self.assertEqual(len(events), 0)

if __name__ == '__main__':
    unittest.main()
