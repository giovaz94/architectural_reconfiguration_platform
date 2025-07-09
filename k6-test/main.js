import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    ramping_requests: {
      executor: 'ramping-arrival-rate',
      startRate: 0,
      timeUnit: '1s',
      preAllocatedVUs: 100,
      maxVUs: 1000,
      stages: [
        { target: 500, duration: '30s' }, 
        { target: 500, duration: '2m' }, 
        { target: 0, duration: '30s' }, 
      ],
    },
  },
};

export default function () {
  const res = http.post('http://localhost:63652/request');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}
