// services/eventService.js
import { fetchDetailUser } from "./detailEventService";
const API_BASE_URL = process.env.REACT_APP_API_BACKEND +"events";

// Lấy sự kiện
export const fetchEvents = async () => {
  try {
    const response = await fetch(API_BASE_URL);
    if (!response.ok) throw new Error("Lỗi khi lấy dữ liệu!");

    const data = await response.json();
    const openEvents = data.filter(event => event.status === "Open");

    // Lấy tên user cho từng sự kiện
    const userPromises = openEvents.map(event => fetchDetailUser(event.id_user_payments));
    const userNames = await Promise.all(userPromises);

    return openEvents.map((event, index) => ({
      id: event.id,
      stt: index + 1,
      name: event.name,
      date: event.date,
      id_user_payments: `ID: ${event.id_user_payments} - ${userNames[index] || "Không tìm thấy"}`,
      total_bill: event.total_bill
    }));
  } catch (error) {
    console.error("Lỗi khi fetch dữ liệu:", error);
    return [];
  }
};
// lấy chi tiết sự kiện
export const fetchEventDetail = async (eventid) => {
  try {
    const response = await fetch(`${API_BASE_URL}/${eventid}`);
    if (!response.ok) throw new Error("Lỗi khi lấy dữ liệu chi tiết sự kiện eventService.js!");

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Lỗi khi fetch dữ liệu:", error);
    return null;
  }
};
  
// Hàm gửi yêu cầu POST để thêm sự kiện mới
export const addEvent = async (events) => {
  try {
    console.log("🚀 Gửi yêu cầu POST với dữ liệu:", events); // Log dữ liệu gửi lên API

    const response = await fetch(API_BASE_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(events), // Gửi danh sách sự kiện
    });

    console.log("📩 Phản hồi từ server:", response); // Kiểm tra phản hồi từ server

    if (!response.ok) {
      throw new Error(`Lỗi khi thêm sự kiện: ${response.statusText}`);
    }

    const responseData = await response.json(); // Đọc dữ liệu JSON từ phản hồi
    console.log("✅ Dữ liệu JSON từ API:", responseData); // Kiểm tra nội dung JSON trả về

    return responseData;
  } catch (error) {
    console.error("❌ Lỗi khi gọi API thêm sự kiện:", error);
    return null;
  }
};
// hàm Put events
export const updateEvent = async (eventId, updatedEventData) => {
  try {
    console.log(`🔄 Gửi yêu cầu PUT đến: ${API_BASE_URL}/${eventId}`);
    console.log("📤 Dữ liệu gửi đi:", updatedEventData);

    const response = await fetch(`${API_BASE_URL}/${eventId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedEventData),
    });

    if (!response.ok) {
      throw new Error(`Lỗi khi cập nhật sự kiện: ${response.statusText}`);
    }

    const responseData = await response.json();
    console.log("✅ Phản hồi từ API:", responseData);
    return responseData;
  } catch (error) {
    console.error("❌ Lỗi khi gọi API cập nhật sự kiện:", error);
    return null;
  }
};