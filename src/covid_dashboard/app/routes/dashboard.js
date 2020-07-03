import Route from '@ember/routing/route';
import { tracked } from '@glimmer/tracking';

class Locale {
    constructor(name, population) {
        this.name = name;
        this.population = population;
    }
}

export default class DashboardRoute extends Route {
    model() {
        return this.store.findAll('state');;
    }
}