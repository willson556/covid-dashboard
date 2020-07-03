import Service from '@ember/service';
import { tracked } from '@glimmer/tracking';

export default class ConfigService extends Service {
    @tracked states = [];
    @tracked counties = [];
    @tracked plots = [];
}