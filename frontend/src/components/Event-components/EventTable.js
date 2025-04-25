import React from "react";
import { updateEvent } from "../../services/eventService";
import { Link } from "react-router-dom";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
} from "@mui/material";

const EventTable = ({ events, setShowEditPopup, deleteEvent, togglePaid }) => {
  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Số thứ tự</TableCell>
            <TableCell>ID</TableCell>
            <TableCell>Tên sự kiện</TableCell>
            <TableCell>Ngày tạo</TableCell>
            <TableCell>Giá bill</TableCell>
            <TableCell>Tên người thanh toán</TableCell>
            <TableCell>Hành động</TableCell>
            <TableCell>Trạng thái</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {events.map((event, index) => (
            <TableRow key={event.id || index}>
              <TableCell>{event.stt}</TableCell>
              <TableCell>{event.id}</TableCell>
              <TableCell>{event.name}</TableCell>
              <TableCell>{event.date}</TableCell>
              <TableCell>{event.total_bill}</TableCell>
              <TableCell>{event.id_user_payments}</TableCell>
              <TableCell>          
                <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                  <Button
                    variant="contained"
                    color="primary"
                    component={Link}
                    to={`/events/${event.id}`}
                    target="_blank"
                    size="small" // Giảm kích thước nút để vừa hàng
                  >
                    Đi đến sự kiện
                  </Button>
                  <Button
                    variant="contained"
                    color="warning"
                    onClick={() => setShowEditPopup({ statuss: true, eventid: event.id })}
                    size="small"
                  >
                    Chỉnh sửa
                  </Button>
                  <Button
                    variant="contained"
                    color="error"
                    onClick={() => {
                      deleteEvent(event.id);
                      updateEvent(event.id, { status: "notOpen" });
                    }}
                    size="small"
                  >
                    X
                  </Button>
                </div>
              </TableCell>
              <TableCell>
                <Button
                  variant="outlined"
                  color={event.paid_status ? "success" : "error"}
                  onClick={() => togglePaid(event.id)}
                >
                  {event.paid_status ? "Paid" : "UnPaid"}
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default EventTable;
