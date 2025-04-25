
import React, { useState, useEffect } from "react";
import { Button, Container, Typography } from "@mui/material";
import { fetchEvents, addEvent, updateEvent } from "../services/eventService";
import EventTable from "../components/Event-components/EventTable";
import AddEventPopup from "../components/Event-components/AddEventPopup";
import EditEventPopup from "../components/Event-components/EditEventPopup";

function EventPage() {
  const [showAddPopup, setShowAddPopup] = useState(false);
  const [showEditPopup, setShowEditPopup] = useState({ statuss: false, eventid: null });
  const [events, setEvents] = useState([]);
  const [newEvent, setNewEvent] = useState({ name: "", date: "", total_bill: "", id_user_payments: "" });

  useEffect(() => {
    fetchEvents().then(setEvents);
  }, []);

  const handleInputChange = (e) => {
    setNewEvent({ ...newEvent, [e.target.name]: e.target.value });
  };

  const handleAddEvent = async () => {
    if (!newEvent.name || !newEvent.date || !newEvent.total_bill || !newEvent.id_user_payments) {
      alert("Vui lòng nhập đầy đủ thông tin!");
      return;
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString);
      const day = String(date.getDate()).padStart(2, "0");
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const year = date.getFullYear();
      return `${day}-${month}-${year}`;
    };

    const formattedEvent = {
      ...newEvent,
      date: formatDate(newEvent.date),
    };

    const eventList = [formattedEvent];
    const addedEvent = await addEvent(eventList);

    if (addedEvent) {
      setEvents(await fetchEvents());
      setShowAddPopup(false);
      setNewEvent({ name: "", date: "", total_bill: "", id_user_payments: "" });
    } else {
      alert("Lỗi khi thêm sự kiện!");
    }
  };

  const handleUpdateEvent = async () => {
    if (!showEditPopup.eventid) {
      alert("Không tìm thấy sự kiện để cập nhật!");
      return;
    }

    const updatedEvent = {};
    if (newEvent.name) updatedEvent.name = newEvent.name;
    if (newEvent.total_bill) updatedEvent.total_bill = newEvent.total_bill;
    if (newEvent.id_user_payments) updatedEvent.id_user_payments = newEvent.id_user_payments;
    if (newEvent.status !== undefined) updatedEvent.status = newEvent.status;

    if (newEvent.date) {
      const formatDate = (dateString) => {
        const date = new Date(dateString);
        const day = String(date.getDate()).padStart(2, "0");
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const year = date.getFullYear();
        return `${day}-${month}-${year}`;
      };
      updatedEvent.date = formatDate(newEvent.date);
    }

    const result = await updateEvent(showEditPopup.eventid, updatedEvent);

    if (result) {
      setEvents(await fetchEvents());
      setShowEditPopup(false);
      setNewEvent({ name: "", date: "", total_bill: "", id_user_payments: "" });
    } else {
      alert("Lỗi khi cập nhật sự kiện!");
    }
  };

  const deleteEvent = (id) => {
    setEvents(events.filter(event => event.id !== id));
  };

  const togglePaid = (id) => {
    setEvents(events.map(event => event.id === id ? { ...event, paid_status: !event.paid_status } : event));
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Welcome to the Event Page!
      </Typography>
      <Button variant="contained" color="primary" onClick={() => setShowAddPopup(true)}>
        Add Event
      </Button>
      <EventTable events={events} setShowEditPopup={setShowEditPopup} deleteEvent={deleteEvent} togglePaid={togglePaid} />
      <AddEventPopup showAddPopup={showAddPopup} setShowAddPopup={setShowAddPopup} newEvent={newEvent} handleInputChange={handleInputChange} addEvent={handleAddEvent} setNewEvent={setNewEvent} />
      <EditEventPopup showEditPopup={showEditPopup} setShowEditPopup={setShowEditPopup} newEvent={newEvent} handleInputChange={handleInputChange} updateEvent={handleUpdateEvent} setNewEvent={setNewEvent} />
    </Container>
  );
}

export default EventPage;
