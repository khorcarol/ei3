import { useState , useEffect} from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios'

function App() {
  const [data, setData] = useState([]);

  const fetchData = async () =>{
    const response = await axios.get("http://localhost:3000/data/1");
    setData(response.data.data);
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <>
      {data.map((item, index) => (
        <li key={index}>
          Sensor ID: {item.sensor_id}, Timestamp: {item.timestamp_to}
        </li>
      ))}
    </>
  );
}

export default App
