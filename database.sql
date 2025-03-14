\c dangt
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email_teams VARCHAR(255) NOT NULL,
    sdt VARCHAR(255) NOT NULL,
    ten_nh VARCHAR(255),
    stk VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
);


CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date TIMESTAMP NOT NULL,
    total_bill INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE event_user (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    bonusThem INTEGER NOT NULL,
    bill_due INTEGER NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Áp dụng trigger cho bảng users
CREATE TRIGGER trigger_update_users
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Áp dụng trigger cho bảng events
CREATE TRIGGER trigger_update_events
BEFORE UPDATE ON events
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

INSERT INTO users (name, email_teams, sdt, qr_code)
VALUES 
('Nguyễn Văn A', 'nguyenvana@teams.com', '0987654321', NULL),
('Trần Thị B', 'tranthib@teams.com', '0977123456', NULL),
('Lê Văn C', 'levanc@teams.com', '0912345678', NULL);


INSERT INTO events (name, date, total_bill)
VALUES 
('lẩu', '2024-03-10', 5000000),
('cafe', '2024-03-15', 8000000),
('nướng', '2024-03-20', 3000000);

INSERT INTO event_user (event_id, user_id, bonusThem, bill_due, status)
VALUES 
(1, 1, 500000, 1000000, 'Đã thanh toán'),
(1, 2, 300000, 700000, 'Chưa thanh toán'),
(2, 3, 800000, 1200000, 'Đã thanh toán'),
(3, 1, 200000, 500000, 'Chưa thanh toán'),
(3, 2, 400000, 900000, 'Đã thanh toán');

SELECT * FROM users;
SELECT * FROM events;
SELECT * FROM event_user;


