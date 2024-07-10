import { Helmet } from 'react-helmet';

const Head = () => {
  return (
    <Helmet>
      {/* Standard Meta Tags */}
      <meta charSet="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta name="description" content="Explore the capabilities of genetic algorithms in solving the Traveling Salesman Problem with this interactive visualization tool." />
      <meta name="keywords" content="Genetic Algorithm, Traveling Salesman Problem, TSP, Optimization, Algorithm, React, Visualization" />
      <meta name="author" content="Miles Exner" />

      {/* Open Graph Meta Tags */}
      <meta property="og:title" content="Genetic Algorithm Visualization Tool" />
      <meta property="og:description" content="Explore the capabilities of genetic algorithms in solving the Traveling Salesman Problem with this interactive visualization tool." />
      <meta property="og:image" content="https://cs-506-algorithms-and-data-structures.vercel.app/genetic-algorithm.jpg" />
      <meta property="og:url" content="https://cs-506-algorithms-and-data-structures.vercel.app" />
      <meta property="og:type" content="website" />
      <meta property="og:site_name" content="Genetic Algorithm Visualization Tool" />

      {/* Twitter Meta Tags */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content="Genetic Algorithm Visualization Tool" />
      <meta name="twitter:description" content="Explore the capabilities of genetic algorithms in solving the Traveling Salesman Problem with this interactive visualization tool." />
      <meta name="twitter:image" content="https://cs-506-algorithms-and-data-structures.vercel.app/genetic-algorithm.jpg" />
      <meta name="twitter:site" content="@dizolivemint" />
      <meta name="twitter:creator" content="@dizolivemint" />

      <title>Genetic Algorithm Visualization Tool</title>
    </Helmet>
  );
};

export default Head;
