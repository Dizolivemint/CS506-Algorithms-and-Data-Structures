import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Polyline, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import styled from 'styled-components';
import L from 'leaflet';
import Loader from './components/loader';
import Tooltip from './components/tooltip';
import { Collapse } from 'react-collapse';

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
  gap: 10px;

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
  width: clamp(50px, 6vw, 150px);
`;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  @media (max-width: 900px) {
    width: 100%;
  }
`;

const SubContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-top: 1rem;
`;

const Label = styled.label`
  margin: 5px 0;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  position: relative;
  min-height: 50px;
  width: 100%;
`;

const Input = styled.input`
  margin: 5px 0;
  padding: 10px;
  font: 'Nunito', sans-serif;
  font-size: clamp(1rem, 1.5vw, 2rem);
  width: clamp(3rem, 5vw, 8rem);
`;

const Button = styled.button`
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font: 'Nunito', sans-serif;
  font-size: clamp(1rem, 1.5vw, 2rem);
`;

const AccordionButton = styled.button`
  width: 100%;
  text-align: center;
  padding: 10px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  font: 'Nunito', sans-serif;
  font-size: clamp(1rem, 1.5vw, 2rem);
  border-radius: 5px
`;

const RouteList = styled.div`
  text-align: left;
  display: flex;
  flex-direction: column;

  & p {
    padding: 10px 0;
    margin: 0;
    border-top: 1px solid #dfdfdf;
  }
`;

const CustomCheckbox = styled.input.attrs({ type: 'checkbox' })`
  width: 40px;
  height: 40px;
  appearance: none;
  background-color: #fff;
  border: 2px solid #007bff;
  border-radius: 4px;
  cursor: pointer;
  margin: 20px 0;

  &:checked {
    background-color: #007bff;
  }
`;

const Footer = styled.footer`
  display: flex;
  flex-direction: column;
  border-top: 1px solid #dfdfdf;
  padding: 20px;
  margin-top: 20px;
  width: 100%;

  & h2 {
    margin-bottom: 10px;
    text-align: center;
    border-bottom: 1px solid #dfdfdf;
    padding-bottom: 10px;
    margin-bottom: 20px;
  }

  & ul {
    display: flex;
    flex-direction: column;
    list-style: none;
    align-self: center;
    margin: 0;
    padding: 0;
    width: clamp(300px, 50vw, 600px);
  }
`;

const Map: React.FC = () => {
  const [solutions, setSolutions] = useState<Solution[]>([]);
  const [currentSolutionIndex, setCurrentSolutionIndex] = useState(0);
  const [popSize, setPopSize] = useState(200);
  const [mutationRate, setMutationRate] = useState(0.01);
  const [crossoverRate, setCrossoverRate] = useState(0.7);
  const [usePmx, setUsePmx] = useState(true);
  const [useOx, setUseOx] = useState(true);
  const [useAco, setUseAco] = useState(true);
  const [useSa, setUseSa] = useState(false);
  const [initialTemp, setInitialTemp] = useState<number | undefined>(1000);
  const [coolingRate, setCoolingRate] = useState<number | undefined>(0.995);
  const [iterations, setIterations] = useState<number | undefined>(10000);
  const [pheromoneThreshold, setPheromoneThreshold] = useState<number | undefined>(5);
  const [useElitism, setUseElitism] = useState(true);
  const [fitnessThreshold, setFitnessThreshold] = useState<number | undefined>(undefined);
  const [noImprovementGenerations, setNoImprovementGenerations] = useState(10);
  const [executionTime, setExecutionTime] = useState<number | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isAccordionOpen, setIsAccordionOpen] = useState(false);

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

  const handleBestFirstSearchSubmit = () => {
    setIsSubmitting(true);
    const distanceMatrixString = JSON.stringify(Object.values(distanceMatrix));
    setSolutions([]);

    fetch(`${url}/best-first-search?distance_matrix=${encodeURIComponent(distanceMatrixString)}`)
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
          generation: 3628800,
          fitness: 0,
        };

        setSolutions(prevSolutions => [...prevSolutions, finalSolution]);
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
    }, 200); // Delay in ms between showing each solution

    if (currentSolutionIndex === solutions.length - 1) {
      setIsSubmitting(false);
    }
    return () => clearInterval(interval);
  }, [solutions, currentSolutionIndex]);

  // Update map height and zoom level based on window size
  const mapHeight = window.innerWidth < 900 ? '50vh' : '100vh';
  const mapWidth = window.innerWidth < 900 ? '96%' : '100%';
  const mapZoom = window.innerWidth < 500 ? 3 : window.innerWidth < 900 ? 4 : window.innerWidth < 1400 ? 3.5 : window.innerWidth < 1600 ? 4 : 4;

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
    <Wrapper>
      <Container>
        <Container>
          <Title>
            <h1>Traveling Salesman Problem Visualizer</h1>
            <Avatar src="avatar.png" alt="Portrait of Miles Exner"/>
          </Title>
        </Container>
        <Container>
        <AccordionButton onClick={() => setIsAccordionOpen(!isAccordionOpen)}>
            Genetic Algorithm
          </AccordionButton>
          <Collapse isOpened={isAccordionOpen}>
            <Form onSubmit={handleSubmit}>
              <Label>
                Population Size:
                <SubContainer>
                  <Input type="number" value={popSize} onChange={(e) => setPopSize(Number(e.target.value))} />
                  <Tooltip text="The number of individuals in the population." />
                </SubContainer>
              </Label>
              <Label>
                Mutation Rate:
                <SubContainer>
                  <Input type="number" step="0.01" value={mutationRate} onChange={(e) => setMutationRate(Number(e.target.value))} />
                  <Tooltip text="The probability of mutating each individual." />
                </SubContainer>
              </Label>
              <Label>
                Crossover Rate:
                <SubContainer>
                  <Input type="number" step="0.01" value={crossoverRate} onChange={(e) => setCrossoverRate(Number(e.target.value))} />
                  <Tooltip text="The probability of crossover between individuals." />
                </SubContainer>
              </Label>
              <Label>
                Use PMX:
                <SubContainer>
                  <CustomCheckbox type="checkbox" checked={usePmx} onChange={(e) => setUsePmx(e.target.checked)} />
                  <Tooltip text="Whether to use Partially Mapped Crossover (PMX)." />
                </SubContainer>
              </Label>
              <Label>
                Use OX:
                <SubContainer>
                  <CustomCheckbox type="checkbox" checked={useOx} onChange={(e) => setUseOx(e.target.checked)} />
                  <Tooltip text="Whether to use Order Crossover (OX)." />
                </SubContainer>
              </Label>
              <Label>
                Use Elitism:
                <SubContainer>
                  <CustomCheckbox type="checkbox" checked={useElitism} onChange={(e) => setUseElitism(e.target.checked)} />
                  <Tooltip text="Whether to use elitism (preserve the best individual)." />
                </SubContainer>
              </Label>
              <Label>
                Fitness Threshold:
                <SubContainer>
                  <Input type="number" value={fitnessThreshold} onChange={(e) => setFitnessThreshold(e.target.value ? Number(e.target.value) : undefined)} />
                  <Tooltip text="The fitness value at which the algorithm stops." />
                </SubContainer>
              </Label>
              <Label>
                No Improvement Generations:
                <SubContainer>
                  <Input type="number" value={noImprovementGenerations} onChange={(e) => setNoImprovementGenerations(Number(e.target.value))} />
                  <Tooltip text="The number of generations with no improvement after which the algorithm stops." />
                </SubContainer>
              </Label>
              <Label>
                Ant Colony Optimization:
                <SubContainer>
                  <CustomCheckbox type="checkbox" checked={useAco} onChange={(e) => setUseAco(e.target.checked)} />
                  <Tooltip text="Whether to use Ant Colony Optimization." />
                </SubContainer>
              </Label>
              {useAco && (
                <Label>
                  Pheromone Threshold:
                  <SubContainer>
                    <Input type="number" min={1} max={10} step={1} value={pheromoneThreshold} onChange={(e) => setPheromoneThreshold(e.target.value ? Number(e.target.value) : undefined)} />
                    <Tooltip text="The pheromone value at which the algorithm stops." />
                  </SubContainer>
                </Label>
              )}
              <Label>
                Simulated Annealing:
                <SubContainer>
                  <CustomCheckbox type="checkbox" checked={useSa} onChange={(e) => setUseSa(e.target.checked)} />
                  <Tooltip text="Whether to use Simulated Annealing." />
                </SubContainer>
              </Label>
              {useSa && (
              <>
                <Label>
                  Initial Temperature:
                  <SubContainer>
                    <Input type="number" min={500} max={5000} step={100} value={initialTemp} onChange={(e) => setInitialTemp(e.target.value ? Number(e.target.value) : undefined)} />
                    <Tooltip text="The initial temperature for the annealing process." />
                  </SubContainer>
                </Label>
                <Label>
                  Cooling Rate:
                  <SubContainer>
                    <Input type="number" min={0.9} max={0.999} step={0.001} value={coolingRate} onChange={(e) => setCoolingRate(e.target.value ? Number(e.target.value) : undefined)} />
                    <Tooltip text="The rate at which the temperature decreases." />
                  </SubContainer>
                </Label>
                <Label>
                  Iterations:
                  <SubContainer>
                    <Input type="number" min={1000} max={10000} step={100} value={iterations} onChange={(e) => setIterations(e.target.value ? Number(e.target.value) : undefined)} />
                    <Tooltip text="The number of iterations for the annealing process." />
                  </SubContainer>
                </Label>
              </>
              )}
              {isSubmitting ? <Loader /> : (
                <>
                  <Button type="submit">Run Genetic Algorithm</Button>
                </>
              )}
            </Form>
          </Collapse>
          {isSubmitting ? <Loader /> : (
                <>
                  <Button type="button" onClick={handleBestFirstSearchSubmit}>Best First Search</Button>
                  <Button type="button" onClick={handleBruteForceSubmit}>Brute Force</Button>
                </>
              )}
        </Container>
      </Container>
      
      <Container style={{ width: '100%' }}>
        
        <Container>
          <MapContainer center={[39.8283, -98.5795]} zoom={mapZoom} style={{ height: mapHeight, width: mapWidth }}>
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
        
      </Container>
      <Container style={window.innerWidth < 900 ? { width: '100%' } : { width: '30%' }}>
          <h2>Solutions</h2>
          <RouteList>
            {currentSolution && (
              <>
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
                {/* <p><b>Execution Time:</b> {executionTime ? `${executionTime} ms` : 'N/A'}</p> */}
              </>
            )}
          </RouteList>
        </Container>
    </Wrapper>
    <Footer>
          <h2>About</h2>
          <ul style={{ listStyle: "none", margin: 0 }}>
            <li>Portfolio Project for CS506 | Algorithms and Data Structures<hr></hr></li>
            <li>Implemented Best First Search for CS510 | Foundations of AI</li>
            <li>Source available on <a href="https://github.com/Dizolivemint/CS506-Algorithms-and-Data-Structures">GitHub</a><hr></hr></li>
            <li>Consult me on your next project through <a href='https://www.linkedin.com/in/milesexner/'>LinkedIn</a><hr></hr></li>
            <li>&copy; {year} Miles Exner. All rights reserved</li>
          </ul>
        </Footer>
    </>
  );
};

export default Map;
