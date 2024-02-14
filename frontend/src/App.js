import React, { useState, useEffect } from 'react';
import axios from "axios";
// import { useNavigate } from "react-router-dom";

function App() {
  const [data, setData] = useState([]);
  // const navigate = useNavigate();

  useEffect(() => {
    axios.get("/getTasks")
    .then((res) => {
      setData(res.data);
      // console.log(res.data[0])
      // console.log(res.data);
    })
    .catch((error) => {
      console.log(error);
    })
  }, []);

  const finish = (id) => {
    axios.get("/delete/"+id)
    .then(res => {
      // navigate("/");
      window.location.reload();
    })
    .catch((error) => {
      console.log(error);
    })
  }

  return (
    <div>
      <h1> Tasks </h1>
      <form action="/addTask" method="POST">
        <label> Priority: </label>
         <input type="number" name="priority" placeholder="Enter Number from 1-3..." min="1" max="3"></input>
         <label> Task: </label>
         <input type="text" name= "task" placeholder="task..."></input> <br></br><br></br>
         <label> Date: </label>
         <input type="date" name="date"></input>
         <label> Time: </label>
         <input type="time" name="time"></input> <button type="submit">Add</button>
      </form> <br></br>

      { data.length > 0 ? (
        data.map((group) => (
          <>
          <h3>
          {group[0].today 
          ? ("Today: " + group[0].datetime.substring(0, group[0].datetime.length-13)) 
          : ( group[0].datetime.substring(0, group[0].datetime.length-13))}
          </h3>
          
          <table border="1px">
          <th> Priority </th>
          <th> Task </th>
          <th> Time </th>
          <th>  </th>
          
            {group.map((item) => (
              
              <tr>
              <td>{item.priority}</td>
              <td>{item.task}</td>
              <td>{item.time}</td>
              <td><button onClick={() => finish(item.id)} type="button">Finish</button></td>
              </tr>
              
            ))}
          </table>
          <br></br><br></br>
          </>
          
        ))
        
        ) : (
          <p>No tasks</p>
        )}
      
    </div>
  )
  // data.length === 0 ? "Loading" : (
  //   <div>
  //     {/* Content: { data } */}
  //     {/* Content: {data[1]["age"]} */}
  //     { data[1]['age'] }
      
  //   </div>
  // )
  
}

export default App