import React, { useEffect, useState } from 'react';
import axios from 'axios';

const DesireTimeline = ({ userId }) => {
  const [roadmap, setRoadmap] = useState([]);
  const [horizon, setHorizon] = useState(3);

  useEffect(() => {
    axios.get(`/api/roadmap/${userId}?horizon=${horizon}`)
      .then(res => setRoadmap(res.data.roadmap))
      .catch(err => console.error(err));
  }, [userId, horizon]);

  return (
    <div className="timeline-container">
      <h2>Моя дорожная карта желаний</h2>
      <select value={horizon} onChange={e => setHorizon(Number(e.target.value))}>
        <option value={3}>3 года</option>
        <option value={5}>5 лет</option>
        <option value={10}>10 лет</option>
      </select>
      <div className="timeline">
        {roadmap.map((item, idx) => (
          <div key={idx} className="timeline-item">
            <div className="year">{item.year}</div>
            <div className="category">{item.category}</div>
            <div className="description">{item.description}</div>
            <div className="confidence">Вероятность: {(item.confidence * 100).toFixed(0)}%</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DesireTimeline;
