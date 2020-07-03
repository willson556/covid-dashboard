import Service from '@ember/service';
import { tracked } from '@glimmer/tracking';

export class Plot {
    id = 0;
    name = '';

    constructor(id, name) {
        this.id = id;
        this.name = name;
    }
}

export default class ConfigService extends Service {
    @tracked states = [];
    @tracked counties = [];
    @tracked plots = [];

    availablePlots = [
        new Plot(0, "Deaths per Day"),
        new Plot(1, "Cases per Day"),
        new Plot(2, "Hospitalizations"),
        new Plot(3, "Positive Test Rate"),
    ];
}