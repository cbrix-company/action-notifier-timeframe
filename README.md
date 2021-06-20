# action-notifier-timeframe

This action is designed to limit executions of actions/steps using timeframe caching with the [actions/cache](https://github.com/actions/cache) action.

## Background

The actions/cache action allows for caching files for each run using a cache key pattern.

```yaml
name: Caching with npm

on: push

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Cache node modules
        uses: actions/cache@v2
        env:
          cache-name: cache-node-modules
        with:
          path: ~/.npm
          key: ${{ runner.os }}-build-${{ env.cache-name }}-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-build-${{ env.cache-name }}-
            ${{ runner.os }}-build-
            ${{ runner.os }}-

      - name: Install Dependencies
        run: npm install

      - name: Build
        run: npm build

      - name: Test
        run: npm test
```

This would cache or restore node modules for a specific package-lock.json hash key.

We will leverage this mechanism to set cache keys with specific time frame. This will allow a certain action to be performed once within a timeframe.

You can use this mechanism e.g. to limit the amount of notifications you want to send with another action

```yaml
name: Notification

on: [push]

jobs:
  Bandit:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Set timeframe
      uses: cbrix-company/action-notifier-timeframe@v1.0.3
      id: timeframe
      with:
        time-unit: minutes
        interval: 5

    - name: Notify Cache
      id: cache
      uses: actions/cache@v2
      with:
        path: ~/timeframe-locks
        key: ${{ github.repository }}-${{ steps.timeframe.outputs.timeframe }}

    - name: Notify
      if: steps.cache.outputs.cache-hit != 'true'
      run: echo "NOTIFY!"
```

## Example settings

Here are some examples showing you how the cache hits using a timeframe key

### Every 5 minutes

```yaml
- name: Set timeframe
    uses: cbrix-company/action-notifier-timeframe@v1.0.3
    id: timeframe
    with:
    time-unit: minutes
    interval: 5
```

| Timeframe     | Current time  | Cache hit  |
| ------------- |:-------------:| -----:|
| 15:00-15:05   | 15:01         | <span style="color:red">X</span>     |
| 15:00-15:05   | 15:02         | <span style="color:green">V</span>     |
| 15:00-15:05   | 15:03         | <span style="color:green">V</span>     |
| 15:00-15:05   | 15:04         | <span style="color:green">V</span>     |
| 15:05-15:10   | 15:05         | <span style="color:red">X</span>     |
| 15:05-15:10   | 15:05         | <span style="color:green">V</span> |

### Every 30 minutes

```yaml
- name: Set timeframe
    uses: cbrix-company/action-notifier-timeframe@v1.0.3
    id: timeframe
    with:
    time-unit: minutes
    interval: 30
```

| Timeframe     | Current time  | Cache hit  |
| ------------- |:-------------:| -----:|
| 15:00-15:30   | 15:00         | <span style="color:red">X</span>     |
| 15:00-15:30   | 15:15         | <span style="color:green">V</span>     |
| 15:30-16:00   | 15:30         | <span style="color:red">X</span>     |


## Downsides

The timeframe caching mechanism is not like rate limiting based on exact time difference calculations.

Lets say you have the following configuration

```yaml
- name: Set timeframe
    uses: cbrix-company/action-notifier-timeframe@v1.0.3
    id: timeframe
    with:
    time-unit: minutes
    interval: 60
```

Two executions could happen close to each other when the cache is cold.

| Timeframe     | Current time  | Cache hit  |
| ------------- |:-------------:| -----:|
| 15:00-16:00   | 15:59         | <span style="color:red">X</span>     |
| 16:00-17:00   | 16:00         | <span style="color:red">X</span>     |
