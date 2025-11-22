async function fetchData() {
    const response = await fetch('https://source-endpoint.com/data');
    return response.json();
  }
  
  async function sendData(data: any) {
    const response = await fetch('https://target-endpoint.com/api', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    return response.status === 200 ? true : false;
  }
  
  async function exchangeData() {
    const data = await fetchData();
    await sendData(data);
  }
  
  exchangeData();
  