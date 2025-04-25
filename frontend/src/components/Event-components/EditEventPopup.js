import React, { useEffect, useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Autocomplete,
} from "@mui/material";
import { useFetchUsers } from "../../hooks/userList";
import { addUserToEvent, updateUserStatus } from "../../services/detailEventService";
import { fetchEventDetail } from "../../services/eventService";

const EditEventPopup = ({
  showEditPopup,
  setShowEditPopup,
  newEvent,
  handleInputChange,
  updateEvent,
  setNewEvent,
}) => {
  const { users, loading } = useFetchUsers();
  const [oldUserPayment, setOldUserPayment] = useState(null);

  useEffect(() => {
    const fetchDetail = async () => {
      if (showEditPopup.statuss && showEditPopup.eventid) {
        const eventDetail = await fetchEventDetail(showEditPopup.eventid);
  
        //Chuyển đổi định dạng ngày ở đây
        const formattedDate = convertToDateInputFormat(eventDetail.date);
        setOldUserPayment(eventDetail.id_user_payments); // ✅ Lưu lại người cũ
        setNewEvent({ ...eventDetail, date: formattedDate });
      }
    };
    fetchDetail();
  }, [showEditPopup.statuss, showEditPopup.eventid, setNewEvent]);
  
  // Hàm chuyển đổi "18-04-2025" => "2025-04-18"
  const convertToDateInputFormat = (dateString) => {
    const [day, month, year] = dateString.split("-");
    return `${year}-${month}-${day}`;
  };

  if (!showEditPopup.statuss) return null;
  // console.log("🚀 ~ file: EditEventPopup.js:20 ~ EditEventPopup ~ newEvent:", newEvent);
  return (
    <Dialog
      open={showEditPopup.statuss}
      onClose={() => setShowEditPopup({ statuss: false, eventid: null })}
    >
      <DialogTitle>Sửa sự kiện</DialogTitle>
      <DialogContent>
        <TextField
          fullWidth
          margin="dense"
          label="Tên sự kiện"
          name="name"
          value={newEvent.name || ""}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          margin="dense"
          type="date"
          name="date"
          value={newEvent.date || ""}
          onChange={handleInputChange}
          InputLabelProps={{ shrink: true }}
        />
        <TextField
          fullWidth
          margin="dense"
          label="Giá bill"
          name="total_bill"
          value={newEvent.total_bill || ""}
          onChange={handleInputChange}
        />
        <Autocomplete
          options={users}
          getOptionLabel={(option) => option.name}
          loading={loading}
          value={
            users.find((user) => user.id === newEvent.id_user_payments) || null
          }
          onChange={(event, newValue) => {
            handleInputChange({
              target: {
                name: "id_user_payments",
                value: newValue ? newValue.id : "",
              },
            });
          }}
          renderInput={(params) => (
            <TextField
              {...params}
              fullWidth
              margin="dense"
              label="Người thanh toán"
            />
          )}
        />
      </DialogContent>
      <DialogActions>
        <Button
          onClick={() => setShowEditPopup({ statuss: false, eventid: null })}
          color="secondary"
        >
          Hủy
        </Button>
        <Button
          onClick={async () => {
            await updateEvent();
            await addUserToEvent(showEditPopup.eventid, {
              list_user: [newEvent.id_user_payments],
            });
            
            
            await updateUserStatus(showEditPopup.eventid,oldUserPayment, "UnPaid");
              
            
            await updateUserStatus(showEditPopup.eventid,newEvent.id_user_payments, "Người đã thanh toán");
            setShowEditPopup({ statuss: false, eventid: null });
          }}
          color="primary"
          variant="contained"
        >
          Lưu
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default EditEventPopup;
