import { defineBackend } from '@aws-amplify/backend';
import { data } from './data/resource';
import { CfnOutput } from 'aws-cdk-lib';
import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

// ES module equivalent of __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load deployment config for unique export names
const configPath = path.join(__dirname, '..', 'deployment-config.json');
const deploymentConfig = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
const deploymentId = deploymentConfig.deploymentId;

const backend = defineBackend({
  data,
});

// Table exports with deployment ID
new CfnOutput(backend.stack, 'UserProfileTableNameExport', {
  value: backend.data.resources.tables['UserProfile'].tableName,
  exportName: `ConciergeAgent-${deploymentId}-Data-UserProfileTableName`,
  description: 'DynamoDB UserProfile table name (unique per deployment)'
});

new CfnOutput(backend.stack, 'ItineraryTableNameExport', {
  value: backend.data.resources.tables['Itinerary'].tableName,
  exportName: `ConciergeAgent-${deploymentId}-Data-ItineraryTableName`,
  description: 'DynamoDB Itinerary table name (unique per deployment)'
});

new CfnOutput(backend.stack, 'FeedbackTableNameExport', {
  value: backend.data.resources.tables['Feedback'].tableName,
  exportName: `ConciergeAgent-${deploymentId}-Data-FeedbackTableName`,
  description: 'DynamoDB Feedback table name (unique per deployment)'
});
