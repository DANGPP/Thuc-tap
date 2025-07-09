import { fetchDetailUser } from "./detailEventService";
const API_BASE_URL = process.env.REACT_APP_API_BACKEND + "events";

// Lấy danh sách sự kiện (có token)
export const fetchEvents = async () => {
  const token = localStorage.getItem("token");

  try {
    const response = await fetch(API_BASE_URL, {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!response.ok) throw new Error("Lỗi khi lấy dữ liệu!");

    const data = await response.json();
    const openEvents = data.filter(event => event.status === "Open");

    const userPromises = openEvents.map(event =>
      fetchDetailUser(event.id_user_payments)
    );
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

// Lấy chi tiết sự kiện theo ID
export const fetchEventDetail = async (eventid) => {
  const token = localStorage.getItem("token");

  try {
    const response = await fetch(`${API_BASE_URL}/${eventid}`, {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!response.ok) throw new Error("Lỗi khi lấy dữ liệu chi tiết sự kiện!");

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Lỗi khi fetch dữ liệu:", error);
    return null;
  }
};

// Thêm sự kiện mới (POST)
export const addEvent = async (events) => {
  const token = localStorage.getItem("token");

  try {
    console.log("🚀 Gửi yêu cầu POST với dữ liệu:", events);

    const response = await fetch(API_BASE_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(events)
    });

    console.log("📩 Phản hồi từ server:", response);

    if (!response.ok) {
      throw new Error(`Lỗi khi thêm sự kiện: ${response.statusText}`);
    }

    const responseData = await response.json();
    console.log("✅ Dữ liệu JSON từ API:", responseData);
    return responseData;
  } catch (error) {
    console.error("❌ Lỗi khi gọi API thêm sự kiện:", error);
    return null;
  }
};

// Cập nhật sự kiện (PUT)
export const updateEvent = async (eventId, updatedEventData) => {
  const token = localStorage.getItem("token");

  try {
    console.log(`🔄 Gửi yêu cầu PUT đến: ${API_BASE_URL}/${eventId}`);
    console.log("📤 Dữ liệu gửi đi:", updatedEventData);

    const response = await fetch(`${API_BASE_URL}/${eventId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(updatedEventData)
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
