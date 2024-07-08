import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Polyline, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import styled, { createGlobalStyle } from 'styled-components';
import L from 'leaflet';
import Loader from './components/loader';
import Tooltip from './components/tooltip';

const GlobalStyle = createGlobalStyle`
  @import url('https://fonts.googleapis.com/css2?family=Maven+Pro:wght@400;700&family=Nunito:wght@300;400;600;700&display=swap');

  body {
    font-family: 'Nunito', sans-serif;
    font-size: clamp(1rem, 1.5vw, 2rem);
    
  }

  h2 {
    font-family: 'Maven Pro', sans-serif;
  }

  label, input, button {
    font-family: 'Nunito', sans-serif;
    font-size: clamp(1rem, 1.5vw, 2rem);
  }
`;

interface Solution {
  generation: number;
  route: number[];
  distance: number;
  fitness: number;
}

const year = new Date().getFullYear();

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

  @media (max-width: 900px) {
    flex-direction: column;
  }

  & h2 {
    border-bottom: 1px solid #dfdfdf;
    padding-bottom: 10px;
    margin-bottom: 20px;
  }
`;

const Title = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  border-bottom: 1px solid #dfdfdf;
  padding-bottom: 10px;
  margin-bottom: 20px;

`;

const Avatar = styled.img`
  border: 4px solid #dfdfdf;
  border-radius: 50%;
  width: 50px;
`;

const Container = styled.div`
  display: flex;
  flex-direction: column;
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
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
`;

const Input = styled.input`
  margin: 5px 0;
  padding: 10px;
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

const CustomCheckbox = styled.input.attrs({ type: 'checkbox' })`
  width: 40px;
  height: 40px;
  appearance: none;
  background-color: #fff;
  border: 2px solid #007bff;
  border-radius: 4px;
  cursor: pointer;
  position: relative;

  &:checked {
    background-color: #007bff;
  }
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
  const [isSubmitting, setIsSubmitting] = useState(false);

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
    setIsSubmitting(true);

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
    setIsSubmitting(true);
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
            setIsSubmitting(false);
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

    if (currentSolutionIndex === solutions.length - 1) {
      setIsSubmitting(false);
    }
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
    <>
      <GlobalStyle />
      <Wrapper>
        <Container>
          <Container>
            <Title>
              <h1>Traveling Salesman Problem Visualizer</h1>
              <Avatar src="avatar.png" alt="USA Map" style={{ width: '50px' }} />
            </Title>
            <img src="genetic-algorithm.webp" alt="USA Map" style={{ width: '100%' }} />
          </Container>
          <Container>
            <h2>Genetic Algorithm Parameters</h2>
            <Form onSubmit={handleSubmit}>
              <Label>
                Population Size:
                <Input type="number" value={popSize} onChange={(e) => setPopSize(Number(e.target.value))} />
                <Tooltip text="The number of individuals in the population." />
              </Label>
              <Label>
                Mutation Rate:
                <Input type="number" step="0.01" value={mutationRate} onChange={(e) => setMutationRate(Number(e.target.value))} />
                <Tooltip text="The probability of mutating each individual." />
              </Label>
              <Label>
                Crossover Rate:
                <Input type="number" step="0.01" value={crossoverRate} onChange={(e) => setCrossoverRate(Number(e.target.value))} />
                <Tooltip text="The probability of crossover between individuals." />
              </Label>
              <Label>
                Use PMX:
                <CustomCheckbox type="checkbox" checked={usePmx} onChange={(e) => setUsePmx(e.target.checked)} />
                <Tooltip text="Whether to use Partially Mapped Crossover (PMX)." />
              </Label>
              <Label>
                Use OX:
                <CustomCheckbox type="checkbox" checked={useOx} onChange={(e) => setUseOx(e.target.checked)} />
                <Tooltip text="Whether to use Order Crossover (OX)." />
              </Label>
              <Label>
                Use Elitism:
                <CustomCheckbox type="checkbox" checked={useElitism} onChange={(e) => setUseElitism(e.target.checked)} />
                <Tooltip text="Whether to use elitism (preserve the best individual)." />
              </Label>
              <Label>
                Fitness Threshold:
                <Input type="number" value={fitnessThreshold} onChange={(e) => setFitnessThreshold(e.target.value ? Number(e.target.value) : undefined)} />
                <Tooltip text="The fitness value at which the algorithm stops." />
              </Label>
              <Label>
                No Improvement Generations:
                <Input type="number" value={noImprovementGenerations} onChange={(e) => setNoImprovementGenerations(Number(e.target.value))} />
                <Tooltip text="The number of generations with no improvement after which the algorithm stops." />
              </Label>
              {isSubmitting ? <Loader /> : (
                <>
                  <Button type="submit">Run Genetic Algorithm</Button>
                  <Button type="button" onClick={handleBruteForceSubmit}>Run Brute Force</Button>
                </>
              )}
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
        </Container>
        <Container style={{ width: '100%' }}>
        <Container>
        <MapContainer center={[39.8283, -98.5795]} zoom={5} style={{ height: '100vh', width: '95%' }}>
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
        </Container>
        <Container>
          <h2>About</h2>
          <ul style={{ listStyle: "none", margin: 0 }}>
          <li>Portfolio Project for CS506 | Algorithms and Data Structures<hr></hr></li>
          <li>Source available on <a href="https://github.com/Dizolivemint/CS506-Algorithms-and-Data-Structures">GitHub</a><hr></hr></li>
          <li>Consult me on your next project through <a href='https://www.linkedin.com/in/milesexner/'>LinkedIn</a><hr></hr></li>
          <li>&copy; {year} Miles Exner. All rights reserved</li>
          </ul>
        </Container>
        </Container>
      </Wrapper>
    </>
  );
};

export default Map;
