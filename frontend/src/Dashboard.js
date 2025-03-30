import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, Button, Row, Col } from 'react-bootstrap';

const Dashboard = () => {
  const [data, setData] = useState({
    centers: 0,
    employees: 0,
    classes: 0,
  });

  useEffect(() => {
    // Gọi API Django để lấy dữ liệu
    axios
      .get('http://localhost:8000/management/api/dashboard/')
      .then((response) => {
        // Cập nhật state với dữ liệu từ API
        setData(response.data);
      })
      .catch((error) => {
        console.error('Có lỗi xảy ra khi lấy dữ liệu:', error);
      });
  }, []);

  return (
    <div className="container">
      <h2 className="my-4">Dashboard Quản lý Trung Tâm</h2>
      <Row>
        {/* Card 1: Cơ Sở */}
        <Col md={4}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>Cơ sở</Card.Title>
              <Card.Text>{data.centers}</Card.Text>
            </Card.Body>
          </Card>
        </Col>

        {/* Card 2: Nhân Viên */}
        <Col md={4}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>Nhân viên</Card.Title>
              <Card.Text>{data.employees}</Card.Text>
            </Card.Body>
          </Card>
        </Col>

        {/* Card 3: Lớp Học */}
        <Col md={4}>
          <Card className="text-center">
            <Card.Body>
              <Card.Title>Lớp học</Card.Title>
              <Card.Text>{data.classes}</Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <h3 className="my-4">Lớp học hôm nay</h3>
      <Row>
        {/* Lớp học 1 */}
        <Col md={4}>
          <Card>
            <Card.Body>
              <Card.Title>Alpha 1</Card.Title>
              <Card.Text>
                <strong>Chương trình học:</strong> Toán, Lý, Hóa<br />
                <strong>Học viên:</strong> 3<br />
                <strong>Khai giảng ngày:</strong> 01/08/2019<br />
                <strong>Phòng học:</strong> A1<br />
                <strong>Ngày học:</strong> Thứ 2, Thứ 4
              </Card.Text>
              <Button variant="primary">Xem chi tiết</Button>
            </Card.Body>
          </Card>
        </Col>

        {/* Lớp học 2 */}
        <Col md={4}>
          <Card>
            <Card.Body>
              <Card.Title>Alpha 2</Card.Title>
              <Card.Text>
                <strong>Chương trình học:</strong> Tiếng Anh, Vật lý<br />
                <strong>Học viên:</strong> 2<br />
                <strong>Khai giảng ngày:</strong> 01/09/2019<br />
                <strong>Phòng học:</strong> A2<br />
                <strong>Ngày học:</strong> Thứ 3, Thứ 5
              </Card.Text>
              <Button variant="primary">Xem chi tiết</Button>
            </Card.Body>
          </Card>
        </Col>

        {/* Lớp học 3 */}
        <Col md={4}>
          <Card>
            <Card.Body>
              <Card.Title>KID 08</Card.Title>
              <Card.Text>
                <strong>Chương trình học:</strong> Mầm non<br />
                <strong>Học viên:</strong> 5<br />
                <strong>Khai giảng ngày:</strong> 01/09/2020<br />
                <strong>Phòng học:</strong> B1<br />
                <strong>Ngày học:</strong> Thứ 6
              </Card.Text>
              <Button variant="primary">Xem chi tiết</Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
