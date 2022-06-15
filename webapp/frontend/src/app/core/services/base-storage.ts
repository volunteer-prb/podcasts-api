export interface StorageInterface {
  length(): number;
  clear(): void;
  getItem(key: string): unknown;
  removeItem(key: string): void;
  setItem(key: string, value: unknown): void;
}

export abstract class BaseStorage implements StorageInterface {
  constructor(private storage: Storage) {}

  length(): number {
    return this.storage.length;
  }

  clear() {
    this.storage.clear();
  }

  getItem(key: string): unknown {
    return JSON.parse(this.storage.getItem(key) ?? '{}');
  }

  removeItem(key: string) {
    this.storage.removeItem(key);
  }

  setItem(key: string, value: unknown) {
    this.storage.setItem(key, JSON.stringify(value));
  }
}
