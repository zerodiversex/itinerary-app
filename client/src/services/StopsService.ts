import axios from 'axios';

const BASE_URL = `http://localhost:8080/api/v1/search/`;

export const searchStopsByName = async (name: string) => {
  const response = await axios.get(`${BASE_URL}?field=${name}`);
  return response;
};
