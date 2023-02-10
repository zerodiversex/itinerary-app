import axios from 'axios';

const BASE_URL = `http://localhost:8080/api/v1/trip/`;

export const searchRoutesDepature = async (from: string, to: string, dep: string) => {
  return await axios.get(
    `${BASE_URL}?start_station=${from}&end_station=${to}&departure_time=${dep}`
  );
};

export const searchRoutesArrival = async (from: string, to: string, arr: string) => {
  return await axios.get(`${BASE_URL}?start_station=${from}&end_station=${to}&arrival_time=${arr}`);
};
