import Service from '@ember/service';
import { tracked } from '@glimmer/tracking';

export class Plot {
    id = '';
    name = '';
    yAxisLabel = '';
    perCapitaCorrectionApplies = true;
    stateLevelOnly = false;

    constructor(id, name, yAxisLabel, perCapitaCorrectionApplies, stateLevelOnly) {
        this.id = id;
        this.name = name;
        this.yAxisLabel = yAxisLabel;
        this.perCapitaCorrectionApplies = perCapitaCorrectionApplies;
        this.stateLevelOnly = stateLevelOnly;
    }
}

export default class ConfigService extends Service {
    @tracked states = ['3', '5', '10', '33']; // AZ, CA, FL, NY
    @tracked counties = [];
    @tracked plots = ['positive', 'deaths'];
    @tracked startDate = "2020-03-01";
    @tracked endDate = new Date().toISOString().substring(0, 10);
    @tracked perCapita = true;

    availablePlots = [
        new Plot('positive', "Positive Test Results per Day", "Positive Test Results", true, false),
        new Plot('positiveRate', "Positive Test Rate", "% of Tests Returning a Positive Result", false, true),
        new Plot('deaths', "Deaths per Day", "Deaths", true, false),
        new Plot('hospitalized', "Cumulative Hospitalizations", "Persons in Hospital", true, true),
    ];
}