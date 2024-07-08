import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Polyline, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import styled from 'styled-components';
import L from 'leaflet';

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

const distanceMatrixIndex: string[] = [
  "New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ", "Philadelphia, PA", "San Antonio, TX", "San Diego, CA", "Dallas, TX", "San Jose, CA"
];

const distanceMatrix: { [key: string]: number[] } = {
  "New York, NY": [0, 4488604, 1271038, 2617854, 3872715, 151753, 2931721, 4440447, 2489493, 4721507],
  "Los Angeles, CA": [4488629, 0, 3243342, 2489897, 600181, 4359746, 2175375, 193497, 2310393, 546474],
  "Chicago, IL": [1271275, 3242365, 0, 1727879, 2821547, 1221774, 1929670, 3341754, 1490109, 3475268],
  "Houston, TX": [2620560, 2490351, 1742651, 0, 1892338, 2485166, 316885, 2365857, 384818, 3036490],
  "Phoenix, AZ": [3876123, 598443, 2820787, 1894112, 0, 3768196, 1579591, 570661, 1714608, 1144581],
  "Philadelphia, PA": [151170, 4362075, 1222410, 2489378, 3769117, 0, 2803245, 4336849, 2361017, 4672880],
  "San Antonio, TX": [2930870, 2176051, 1929627, 316608, 1578038, 2795477, 0, 2051556, 440105, 2722189],
  "San Diego, CA": [4441363, 193655, 3342630, 2365208, 571281, 4333436, 2050686, 0, 2185703, 740081],
  "Dallas, TX": [2491477, 2310286, 1491130, 385018, 1712273, 2356084, 440404, 2185791, 0, 2718096],
  "San Jose, CA": [4727992, 547589, 3482706, 3034648, 1144932, 4678491, 2720126, 738897, 2718674, 0],
};

const Wrapper = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: flex-start;
  margin: 20px;

  @media (max-width: 1680px) {
    flex-direction: column;
  }
`;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 20px;
  flex-wrap: wrap;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 20px;
`;

const Label = styled.label`
  margin: 5px 0;
`;

const Input = styled.input`
  margin: 5px 0;
`;

const Button = styled.button`
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
`;

const RouteList = styled.div`
  text-align: left;
`;

const Map: React.FC = () => {
  const [solutions, setSolutions] = useState<Solution[]>([]);
  const [currentSolutionIndex, setCurrentSolutionIndex] = useState(0);
  const [popSize, setPopSize] = useState(100);
  const [mutationRate, setMutationRate] = useState(0.01);
  const [crossoverRate, setCrossoverRate] = useState(0.7);
  const [usePmx, setUsePmx] = useState(false);
  const [useOx, setUseOx] = useState(true);
  const [useElitism, setUseElitism] = useState(false);
  const [fitnessThreshold, setFitnessThreshold] = useState<number | undefined>(undefined);
  const [noImprovementGenerations, setNoImprovementGenerations] = useState(20);
  const [executionTime, setExecutionTime] = useState<number | null>(null);
  const [isGenetic, setIsGenetic] = useState(true);

  const blob = [`,"New York, NY","Los Angeles, CA","Chicago, IL","Houston, TX","Phoenix, AZ","Philadelphia, PA","San Antonio, TX","San Diego, CA","Dallas, TX","San Jose, CA"
    "New York, NY",0,4488604,1271038,2617854,3872715,151753,2931721,4440447,2489493,4721507
    "Los Angeles, CA",4488629,0,3243342,2489897,600181,4359746,2175375,193497,2310393,546474
    "Chicago, IL",1271275,3242365,0,1727879,2821547,1221774,1929670,3341754,1490109,3475268
    "Houston, TX",2620560,2490351,1742651,0,1892338,2485166,316885,2365857,384818,3036490
    "Phoenix, AZ",3876123,598443,2820787,1894112,0,3768196,1579591,570661,1714608,1144581
    "Philadelphia, PA",151170,4362075,1222410,2489378,3769117,0,2803245,4336849,2361017,4672880
    "San Antonio, TX",2930870,2176051,1929627,316608,1578038,2795477,0,2051556,440105,2722189
    "San Diego, CA",4441363,193655,3342630,2365208,571281,4333436,2050686,0,2185703,740081
    "Dallas, TX",2491477,2310286,1491130,385018,1712273,2356084,440404,2185791,0,2718096
    "San Jose, CA",4727992,547589,3482706,3034648,1144932,4678491,2720126,738897,2718674,0`
  ];

  const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  const url = isLocalhost ? 'http://localhost:5000' : 'https://cs506-algorithms-and-data-structures.onrender.com';

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', new Blob(blob, { type: 'text/csv' }));
    formData.append('pop_size', popSize.toString());
    formData.append('mutation_rate', mutationRate.toString());
    formData.append('crossover_rate', crossoverRate.toString());
    formData.append('use_pmx', usePmx.toString());
    formData.append('use_ox', useOx.toString());
    formData.append('use_elitism', useElitism.toString());
    formData.append('fitness_threshold', fitnessThreshold ? fitnessThreshold.toString() : '');
    formData.append('no_improvement_generations', noImprovementGenerations.toString());

    fetch(`${url}/run-ga`, {
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
                const parsedData = JSON.parse(data);
                if (parsedData.total_time) {
                  setExecutionTime(parsedData.total_time);
                } else {
                  const solution: Solution = parsedData;
                  setSolutions(prevSolutions => [...prevSolutions, solution]);
                }
              });

              read();
            });
          })();
        }
      });
  };

  const handleBruteForceSubmit = () => {
    const distanceMatrixString = JSON.stringify(Object.values(distanceMatrix));
    setSolutions([]);

    fetch(`${url}/brute?distance_matrix=${encodeURIComponent(distanceMatrixString)}`)
        .then(response => response.json())
        .then(parsedData => {
            if (parsedData.total_time) {
                setExecutionTime(parsedData.total_time);
            }

            const finalSolution = {
                route: parsedData.final_best_route,
                distance: parsedData.final_best_distance,
                generation: 40320,
                fitness: 0,
            };

            setSolutions([finalSolution]);
        })
        .catch(error => {
            console.error("Error fetching brute force solution:", error);
        });
  };

  useEffect(() => {
    const interval = setInterval(() => {
      if (currentSolutionIndex < solutions.length - 1) {
        setCurrentSolutionIndex(prevIndex => prevIndex + 1);
      }
    }, 1000); // Delay in ms between showing each solution

    return () => clearInterval(interval);
  }, [solutions, currentSolutionIndex]);

  const currentSolution = solutions[currentSolutionIndex] || solutions[solutions.length - 1];
  const routeCoordinates = currentSolution
    ? currentSolution.route.map(cityIndex => cityCoordinates[distanceMatrixIndex[cityIndex]])
    : [];

  // Add line back to the first city to complete the loop
  if (routeCoordinates.length > 0) {
    routeCoordinates.push(routeCoordinates[0]);
  }

  return (
    <Wrapper>
      <Container>
        <Form onSubmit={handleSubmit}>
          <Label>
            Population Size:
            <Input type="number" value={popSize} onChange={(e) => setPopSize(Number(e.target.value))} />
          </Label>
          <Label>
            Mutation Rate:
            <Input type="number" step="0.01" value={mutationRate} onChange={(e) => setMutationRate(Number(e.target.value))} />
          </Label>
          <Label>
            Crossover Rate:
            <Input type="number" step="0.01" value={crossoverRate} onChange={(e) => setCrossoverRate(Number(e.target.value))} />
          </Label>
          <Label>
            Use PMX:
            <Input type="checkbox" checked={usePmx} onChange={(e) => setUsePmx(e.target.checked)} />
          </Label>
          <Label>
            Use OX:
            <Input type="checkbox" checked={useOx} onChange={(e) => setUseOx(e.target.checked)} />
          </Label>
          <Label>
            Use Elitism:
            <Input type="checkbox" checked={useElitism} onChange={(e) => setUseElitism(e.target.checked)} />
          </Label>
          <Label>
            Fitness Threshold:
            <Input type="number" value={fitnessThreshold} onChange={(e) => setFitnessThreshold(e.target.value ? Number(e.target.value) : undefined)} />
          </Label>
          <Label>
            No Improvement Generations:
            <Input type="number" value={noImprovementGenerations} onChange={(e) => setNoImprovementGenerations(Number(e.target.value))} />
          </Label>
          <Button type="submit">Run Genetic Algorithm</Button>
          <Button type="button" onClick={handleBruteForceSubmit}>Run Brute Force</Button>
        </Form>
      </Container>
      <Container>
        <h2>Solutions</h2>
        <RouteList>
          {currentSolution && (
            <>
              <h3>Genetic Route Details</h3>
              <p><b>Generation:</b> {currentSolution.generation}</p>
              {currentSolution.route.map((cityIndex, idx) => {
                const nextCityIndex = currentSolution.route[(idx + 1) % currentSolution.route.length];
                const cityName = distanceMatrixIndex[cityIndex];
                const nextCityName = distanceMatrixIndex[nextCityIndex];
                const cityMatrix = distanceMatrix[cityName];
                const distance = cityMatrix[distanceMatrixIndex.indexOf(nextCityName)];
                return (
                  <p key={idx}><b>{cityName} to {nextCityName}:</b> {distance / 1000} km</p>
                );
              })}
              <p><b>Total:</b> {currentSolution.distance} km</p>
              <p><b>Execution Time:</b> {executionTime ? `${executionTime} ms` : 'N/A'}</p>
              <p><b>Note:</b> there is a delay in the display of each generation. Hence, why the execution time has completed calculating.</p>
            </>
          )}
        </RouteList>
      </Container>
      <MapContainer center={[39.8283, -98.5795]} zoom={5} style={{ height: '100vh', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        />
        {routeCoordinates.length > 0 && (
          <>
            <Polyline positions={routeCoordinates} color="blue" />
            <Marker position={routeCoordinates[0]} icon={L.divIcon({ className: 'start-marker', html: '<div style="background-color: red; width: 10px; height: 10px; border-radius: 50%;"></div>' })}>
              <Popup>
                Start: New York, NY
              </Popup>
            </Marker>
          </>
        )}
      </MapContainer>
    </Wrapper>
  );
};

export default Map;
