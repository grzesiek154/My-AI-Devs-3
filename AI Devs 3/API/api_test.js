const axios = require('axios');

      

  // URL of the txt file
const txtFileUrl = 'https://poligon.aidevs.pl/dane.txt';

async function getData() {
    try {
        const response = await axios.get(txtFileUrl);
        const data = response.data;
        return data;  // Return the text data to be processed later
        
    } catch (error) {
        console.error('Error fetching the file:', error);
    }
}

function sendData(data) {
    return axios.post('https://poligon.aidevs.pl/verify', data)
        .then(response => {
            // The file content is available in response.data
            console.log('File content:', response.data);
        })
        .catch(error => {
            console.error('Error fetching the file:', error);
        });
}

function transformData() {
   return getData().then(data => {
        // Split the fetched data into an array of strings
        if (!data) {
            throw new Error('No data available');
        }
    
        const trimedData = data.trim();
        const dataArray = trimedData.split("\n");
        return dataArray;  // Output the array
    });
}

async function exchangeData(data) {
    // const data = await getData();
    const responseJson = {
        "task": "POLIGON",
        "apikey": "a93604b2-40c5-46bd-b562-8fd8fcd47774",
        "answer": data
    }
    await sendData(responseJson);
}

async function main() {
    try {
        const dataArray = await transformData();
        exchangeData(dataArray)// Output the transformed data array
    } catch (error) {
        console.error('Error:', error);
    }
}




//Exection
main();






  
   