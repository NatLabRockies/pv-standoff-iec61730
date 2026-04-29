const MAPBOX_TOKEN = "pk.eyJ1Ijoic2hpcnViYW5hIiwiYSI6ImNtb2pkbXBzdTAyeTYyb29iOXlkc3c0anoifQ.U99frpox2MqclwCEGNehGQ";

let cache = {};

async function loadScenario(scenario) {
  if (cache[scenario]) return cache[scenario];

  const base = `assets/${scenario}`;

  const metadata = await fetch(`${base}/metadata.json`).then(r => r.json());

  async function loadFloat32(name, length) {
    const buffer = await fetch(`${base}/${name}.bin`).then(r => r.arrayBuffer());
    return new Float32Array(buffer);
  }

  const latitude = await loadFloat32("latitude", metadata.nlat);
  const longitude = await loadFloat32("longitude", metadata.nlon);

  const size = metadata.nlat * metadata.nlon;

  const x = await loadFloat32("x", size);
  const T98_0 = await loadFloat32("T98_0", size);
  const T98_inf = await loadFloat32("T98_inf", size);

  cache[scenario] = {
    metadata,
    latitude,
    longitude,
    x,
    T98_0,
    T98_inf
  };

  return cache[scenario];
}

function nearestIndex(array, value) {
  let best = 0;
  let bestDiff = Infinity;

  for (let i = 0; i < array.length; i++) {
    const diff = Math.abs(array[i] - value);
    if (diff < bestDiff) {
      best = i;
      bestDiff = diff;
    }
  }

  return best;
}

function haversineKm(lat1, lon1, lat2, lon2) {
  const R = 6371.0;
  const toRad = d => d * Math.PI / 180;

  const dlat = toRad(lat2 - lat1);
  const dlon = toRad(lon2 - lon1);

  const a =
    Math.sin(dlat / 2) ** 2 +
    Math.cos(toRad(lat1)) *
    Math.cos(toRad(lat2)) *
    Math.sin(dlon / 2) ** 2;

  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

async function geocodeAddress(query) {
  const url =
    `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(query)}.json` +
    `?access_token=${MAPBOX_TOKEN}` +
    `&country=US` +
    `&limit=1` +
    `&types=address,place,postcode`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Mapbox error: ${response.status}`);
  }

  const data = await response.json();

  if (!data.features || !data.features.length) {
    throw new Error("No location found.");
  }

  const feature = data.features[0];
  const [lon, lat] = feature.center;

  return {
    lat,
    lon,
    label: feature.place_name
  };
}

async function queryDataset() {
  const lat = parseFloat(document.getElementById("lat").value);
  const lon = parseFloat(document.getElementById("lon").value);
  const scenario = document.getElementById("scenario").value;
  const results = document.getElementById("results");

  if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
    results.textContent = "Please enter valid latitude and longitude.";
    return;
  }

  results.textContent = "Loading dataset...";

  const ds = await loadScenario(scenario);

  const iLat = nearestIndex(ds.latitude, lat);
  const iLon = nearestIndex(ds.longitude, lon);

  const nearestLat = ds.latitude[iLat];
  const nearestLon = ds.longitude[iLon];

  const idx = iLat * ds.metadata.nlon + iLon;

  const distanceKm = haversineKm(lat, lon, nearestLat, nearestLon);

  const x = ds.x[idx];
  const T98_0 = ds.T98_0[idx];
  const T98_inf = ds.T98_inf[idx];

  if (distanceKm > 10 || Number.isNaN(x)) {
    results.textContent =
      `Requested point: (${lat.toFixed(4)}, ${lon.toFixed(4)})\n` +
      `No valid grid point found within 10 km.\n` +
      `Nearest available grid point is ${distanceKm.toFixed(2)} km away.`;
    return;
  }

  results.textContent =
    `Scenario: ${scenario}\n` +
    `Requested point: (${lat.toFixed(4)}, ${lon.toFixed(4)})\n` +
    `Nearest grid point: (${nearestLat.toFixed(4)}, ${nearestLon.toFixed(4)})\n` +
    `Nearest grid point distance: ${distanceKm.toFixed(2)} km\n\n` +
    `Standoff distance x: ${x.toFixed(2)} cm\n` +
    `T98_0: ${T98_0.toFixed(2)} °C\n` +
    `T98_inf: ${T98_inf.toFixed(2)} °C`;
}

document.getElementById("queryBtn").addEventListener("click", queryDataset);

document.getElementById("findBtn").addEventListener("click", async () => {
  const address = document.getElementById("address").value;
  const results = document.getElementById("results");

  if (!address.trim()) {
    results.textContent = "Please enter an address.";
    return;
  }

  try {
    results.textContent = "Finding address...";
    const geo = await geocodeAddress(address);

    document.getElementById("lat").value = geo.lat.toFixed(6);
    document.getElementById("lon").value = geo.lon.toFixed(6);

    results.textContent = `Found: ${geo.label}`;
    await queryDataset();
  } catch (err) {
    results.textContent = err.message;
  }
});