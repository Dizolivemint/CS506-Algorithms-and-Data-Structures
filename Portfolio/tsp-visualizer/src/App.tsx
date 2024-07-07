import React, { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';

interface Solution {
  generation: number;
  route: number[];
  distance: number;
  fitness: number;
}

const cityCoordinates: { [key: string]: [number, number] } = {
  "New York, NY": [40.7128, -74.0060],
  "Los Angeles, CA": [34.0522, -118.2437],
  "Chicago, IL": [41.8781, -87.6298],
  "Houston, TX": [29.7604, -95.3698],
  "Phoenix, AZ": [33.4484, -112.0740],
  "Philadelphia, PA": [39.9526, -75.1652],
  "San Antonio, TX": [29.4241, -98.4936],
  "San Diego, CA": [32.7157, -117.1611],
  "Dallas, TX": [32.7767, -96.7970],
  "San Jose, CA": [37.3382, -121.8863],
};

const Map: React.FC = () => {
  const [solutions, setSolutions] = useState<Solution[]>([]);
  const [currentSolutionIndex, setCurrentSolutionIndex] = useState(0);

  useEffect(() => {
    const formData = new FormData();
    formData.append('file', new Blob([`,"New York, NY","Los Angeles, CA","Chicago, IL","Houston, TX","Phoenix, AZ","Philadelphia, PA","San Antonio, TX","San Diego, CA","Dallas, TX","San Jose, CA"
    "New York, NY",0,4488604,1271038,2617854,3872715,151753,2931721,4440447,2489493,4721507
    "Los Angeles, CA",4488629,0,3243342,2489897,600181,4359746,2175375,193497,2310393,546474
    "Chicago, IL",1271275,3242365,0,1727879,2821547,1221774,1929670,3341754,1490109,3475268
    "Houston, TX",2620560,2490351,1742651,0,1892338,2485166,316885,2365857,384818,3036490
    "Phoenix, AZ",3876123,598443,2820787,1894112,0,3768196,1579591,570661,1714608,1144581
    "Philadelphia, PA",151170,4362075,1222410,2489378,3769117,0,2803245,4336849,2361017,4672880
    "San Antonio, TX",2930870,2176051,1929627,316608,1578038,2795477,0,2051556,440105,2722189
    "San Diego, CA",4441363,193655,3342630,2365208,571281,4333436,2050686,0,2185703,740081
    "Dallas, TX",2491477,2310286,1491130,385018,1712273,2356084,440404,2185791,0,2718096
    "San Jose, CA",4727992,547589,3482706,3034648,1144932,4678491,2720126,738897,2718674,0`], { type: 'text/csv' }));
    formData.append('pop_size', '100');
    formData.append('mutation_rate', '0.01');
    formData.append('crossover_rate', '0.7');
    formData.append('use_pmx', 'false');
    formData.append('use_ox', 'true');
    formData.append('use_elitism', 'false');
    formData.append('fitness_threshold', '');
    formData.append('no_improvement_generations', '20');

    fetch('http://localhost:5000/run-ga', {
      method: 'POST',
      body: formData,
    })
    .then(response => {
      const reader = response.body?.getReader();
      const decoder = new TextDecoder("utf-8");

      if (reader) {
        (function read() {
          reader.read().then(({ done, value }) => {
            if (done) {
              return;
            }
            const text = decoder.decode(value);
            const events = text.split("\n\n").filter(Boolean);

            events.forEach(event => {
              const data = event.replace(/^data: /, '');
              const solution: Solution = JSON.parse(data);
              setSolutions(prevSolutions => [...prevSolutions, solution]);
            });

            read();
          });
        })();
      }
    });

  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      if (currentSolutionIndex < solutions.length) {
        setCurrentSolutionIndex((prevIndex) => prevIndex + 1);
      }
    }, 1000); // Delay in ms between showing each solution

    return () => clearInterval(interval);
  }, [solutions, currentSolutionIndex]);

  const currentSolution = solutions[currentSolutionIndex];
  const routeCoordinates = currentSolution
    ? currentSolution.route.map((cityIndex) => Object.values(cityCoordinates)[cityIndex])
    : [];

  return (
    <MapContainer center={[37.7749, -122.4194]} zoom={4} style={{ height: '100vh', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      />
      {routeCoordinates.length > 0 && (
        <Polyline positions={routeCoordinates} color="blue" />
      )}
    </MapContainer>
  );
}

export default Map;
