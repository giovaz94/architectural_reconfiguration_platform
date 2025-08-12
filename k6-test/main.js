import http from 'k6/http';

const workload = [
  16, 33, 50, 66, 83, 100, 116, 133, 150, 166,
  183, 200, 216, 233, 250, 266, 283, 300, 316, 333,
  350, 366, 383, 400, 416, 433, 450, 466, 483, 500,
  500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
  500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
  500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
  500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
  500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
  500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
  500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
  500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
  500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
  500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
  500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
  500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
  500, 483, 466, 450, 433, 416, 400, 383, 366, 350,
  333, 316, 300, 283, 266, 250, 233, 216, 200, 183,
  166, 150, 133, 116, 100, 83, 66, 50, 33, 16
];

// const stages = workload.map(rate => ({
//   target: rate,
//   duration: '1s',
// }));

// export let options = {
//   scenarios: {
//     variable_rps: {
//       executor: 'constant-arrival-rate',
//       startRate: workload[0],
//       timeUnit: '1s',
//       preAllocatedVUs: 600,
//       stages: stages,
//     },
//   },
// };

const scenarios = {};
workload.forEach((rate, i) => {
  scenarios[`second_${i}`] = {
    executor: 'constant-arrival-rate',
    rate: rate,
    timeUnit: '1s',
    duration: '1s',
    startTime: `${i}s`,
    preAllocatedVUs: Math.ceil(rate * 0.1) + 1,
    maxVUs: rate + 10,
  };
});

export let options = {
  scenarios: scenarios
};

export default function () {
  http.post('http://localhost:54476/request')
}